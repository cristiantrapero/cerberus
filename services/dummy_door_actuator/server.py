#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import Ice

CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/services.ice --all'.format(CITISIM_SLICE))
import SmartObject


class ActuatorI(SmartObject.DigitalSink):
    def notify(self, value, source, data, current=None):
        if value:
            time_diff = time.time() - data.timestamp
            if time_diff < 15:
                print("Door opened.\n")
        else:
            print("Door closed.\n")


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ActuatorI()

        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("actuator"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
