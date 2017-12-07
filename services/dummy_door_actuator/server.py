#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class ActuatorI(SmartObject.DigitalSink):
    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        super(self.__class__, self).__init__()

    def notify(self, value, source, metadata, current=None):
        if value:
            time_diff = time.time() - metadata.timestamp
            if time_diff < self.properties.getProperty('DoorActuator.TTL'):
                print("Open door.\n")
            else:
                print("Door closed.\n")


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        properties = broker.getProperties()
        servant = ActuatorI(properties)

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("door-actuator"))

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
