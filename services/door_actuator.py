#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
import Ice
import time
Ice.loadSlice('./slices/services.ice --all -I .')
import SmartObject

class ActuatorI(SmartObject.Actuator):
    def set(self, meta, current=None):
        timeDiff = int(time.time()) - meta.timestamp
        if timeDiff < 15:
            print("Puerta abierta.\n")

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ActuatorI()

        adapter = broker.createObjectAdapter("ActuatorAdapter")
        proxy = adapter.add(servant, broker.stringToIdentity("actuator"))

        print(proxy)
        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

sys.exit(Server().main(sys.argv))
