#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('-I {0} {0}/dharma/scone-wrapper.ice --all'.format('/usr/share/slice'))
CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/services.ice --all'.format(CITISIM_SLICE))
import Semantic  # noqa
import SmartObject  # noqa


class Client(Ice.Application):
    def run(self, args):
        self.scone = self.get_scone(args[1])
        self.compose("command execution by authorised person")
        print("Done.")

    def compose(self, event):
        plan = self.make_schedule(event)
        self.build_plan(plan)

    def get_scone(self, proxy):
        proxy = self.communicator().stringToProxy(proxy)
        sconePrx = Semantic.SconeServicePrx.checkedCast(proxy)
        if not sconePrx:
            raise RuntimeError('Invalid proxy')
        return sconePrx

    def make_schedule(self, event):
        services = []

        # 1. We start looking for the most general event. To fix because this should return nil
        sentence = '(list-causes {' + event + '})'
        action = self.scone.sentence(sentence)  # {execute_authorised_command}
        prerequirements = self.get_prerequirements_for_action(action)

        for p in prerequirements:
            services.append(self.make_schedule(p))

        argument = self.get_argument_for_action(action)
        if argument is not None:
            arg_service = self.get_service_for_argument(argument)
            services.append(arg_service)

        action_service = self.get_service_for_action(action)
        if action_service is not None:
            services.append(action_service)

        if len(services) == 1:
            return services[0]
        return services

    # A. Check if there is a pre-requirement for that action
    def get_prerequirements_for_action(self, action):
        sentence = '(get-the-events-required-for-action ' + action + ')'
        reply = self.scone.sentence(sentence)  # ({command recognition} {person recognition})
        if reply == 'NIL':
            return []

        prerequirements = reply.strip("()").split("}")
        return [x for x in [x.strip(" {") for x in prerequirements] if x]

    def get_argument_for_action(self, action):
        sentence = '(car (get-the-required-argument-for-action ' + action + '))'
        reply = self.scone.sentence(sentence)  # wav; jpg
        if reply == 'NIL':
            return None
        return reply

    # B_1. Geth the proxy for the service that returns that argument
    def get_service_for_argument(self, argument):
        sentence = '(car (get-the-service-proxy-that-returns-an-argument ' + argument + '))'
        reply = self.scone.sentence(sentence)
        if reply == "NIL":
            return None
        return reply.strip("{}")

    def get_service_for_action(self, action):
        sentence = '(get-the-service-proxy-for-action ' + action + ')'
        reply = self.scone.sentence(sentence)
        if reply == "NIL":
            return None
        return reply.strip("{}")

    def build_plan(self, plan):
        pending = []

        observer = None
        for item in plan:
            if not isinstance(item, list):
                if observer is not None:
                    self.connect(observer, item)
                observer = item
            else:
                prx = self.build_plan(item)
                pending.append(prx)

        for p in pending:
            self.connect(p, observer)

        return observer

    def connect(self, observable, observer):
        a = observable.split()[0]
        b = observer.split()[0]
        print("connect '{}' -> '{}'".format(a, b))

        ic = self.communicator()
        observable = ic.stringToProxy(observable)
        #FIXME
        observable = SmartObject.ObservablePrx.uncheckedCast(observable)
        observable.setObserver(observer)


sys.exit(Client().main(sys.argv))
