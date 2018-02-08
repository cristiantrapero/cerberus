#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class ActuatorI(SmartObject.EventSink):
    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        super(self.__class__, self).__init__()

    def notify(self, source, metadata, current=None):
        if (time.time() - metadata.timestamp) < self.properties.getProperty('DoorActuator.TTL'):
            print("Open door.\n")
        else:
            print("Door keep closed.\n")

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

        return 0


sys.exit(Server().main(sys.argv))
