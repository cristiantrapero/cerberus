#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import time
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

from SmartObject import MetadataField

class ActuatorI(SmartObject.EventSink):
    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        super(self.__class__, self).__init__()

    def notify(self, source, metadata, current=None):
        eventTimestamp = int(metadata.get(MetadataField.Timestamp))
        ttl = int(self.properties.getProperty('DoorActuator.TTL'))

        # Control the event TTL
        if (time.time() - eventTimestamp < ttl ):
            print("Open door due to the event generated in {}.\n".format(source))
        else:
            print("Door keep closed by timeout.\n")

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
