#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class ActuatorI(SmartObject.DigitalSink):
    def notify(self, value, source, data, current=None):
        if value:
            time_diff = time.time() - data.timestamp
            if time_diff < Ice.getPropierty(DoorActuator.TimeToLive):
                print("Door opened.\n")
        else:
            print("Door closed.\n")


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ActuatorI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.addWithUUID(servant)

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
