#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import Ice
import time

CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/services.ice --all'.format(CITISIM_SLICE))
import SmartObject


class ActuatorI(SmartObject.DigitalSink):
    def notify(self, value, source, meta, position, current=None):
        timeDiff = int(time.time()) - meta.timestamp
        if timeDiff < 15:
            print("Puerta abierta.\n")


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ActuatorI()

        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("actuator"))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
