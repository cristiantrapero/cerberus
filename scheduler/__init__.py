#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('-I {0} {0}/dharma/scone-wrapper.ice --all'.format('/usr/share/slice'))
import Semantic  # noqa
Ice.loadSlice('-I {0} {0}/citisim/wiring.ice --all'.format('/usr/share/slice'))
import SmartObject


make_schedule(e):
    action = action_for_event(e)
    
    service = service_that_perform(action)
    plan += service

    req_events = req_events_for_action(action)

    for e in req_events:
        subplan = make_schedule(e)
        if may_x_invoke_y(subplan.head_service, service):
            plan += subplan

    return plan


may_x_invoke_y(x, y):
    if x.invoked_iface not in y.provided_ifaces:
        return False

    if x.invoked_caps not in y.accepted_caps:
        return False

    return True


class Scheduler:
    def __init__(self, broker):
        self.broker = broker
        self.scone = self.get_scone('scone')

    def make_schedule(self, event):
        action = self.get_action_for_event(event)  # FIXME: a same event may be caused by several actions
        print(action)
        action_service = self.get_service_for_action(action)
        plan = [action_service]
        pre_events = self.get_prerequirements_for_action(action)
        print(pre_events)
        
        for e in pre_events:
            subplan = self.make_schedule(e))
            if self.syntax_matching(subplan.head, action):
                plan.append(subplan.head)

    # FIXME: it should take provider service, instead of provider_action
    def syntax_matching(self, producer, consumer_action):  
        consumed_argument = self.get_argument_for_action(action)
        # consumed_argument = self.get_consumed_by_service(consumer)
        if argument is None:
            return True

        produced_argument = self.get_produced_by_service(producer)
        return self.is_compatible_call(produced_argument, consumed_argument)

    def get_action_for_event(self, event):
        sentence = '(list-causes {' + event + '})'
        return self.scone.sentence(sentence)

    def get_prerequirements_for_action(self, action):
        sentence = '(get-the-events-required-for-action ' + action + ')'
        reply = self.scone.sentence(sentence)
        
        if reply == 'NIL':
            return []

        prerequirements = reply.strip("()").split("}")
        return [x for x in [x.strip(" {") for x in prerequirements] if x]

    
    def make_schedule_old(self, event):
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
        return

    def get_scone(self, proxy):
        proxy = self.broker.stringToProxy(proxy)
        sconePrx = Semantic.SconeServicePrx.checkedCast(proxy)
        if not sconePrx:
            raise RuntimeError('Invalid proxy')
        return sconePrx


class Client(Ice.Application):
    def run(self, args):
        self.scone = self.get_scone(args[1])
        self.wiring_service = self.get_wiring_service(args[2])
        self.compose("open door")

    def compose(self, event):
        plan = self.make_schedule(event)
        self.build_plan(plan)

    def get_wiring_service(self, proxy):
        proxy = self.communicator().stringToProxy(proxy)
        wiringPrx = SmartObject.WiringServicePrx.checkedCast(proxy)
        if not wiringPrx:
            raise RuntimeError('Invalid proxy')
        return wiringPrx

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
        print("connect '{}' -> '{}'".format(observable, observer))

        self.wiring_service.addObserver(observable, observer)


if __name__ == '__main__':
    sys.exit(Client().main(sys.argv))
