#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import logging
import cv2
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class SnapshotServiceI(citisim.ObservableMixin, SmartObject.SnapshotService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        super(self.__class__, self).__init__()

    def notify(self, source, metadata, current=None):
        self.metadata = metadata
        self.trigger(int(self.properties.getProperty('SnapshotService.Snapshots')),
                     int(self.properties.getProperty('SnapshotService.Delay')))

    def trigger(self, count, delay, current=None):
        if not self.observer:
            logging.error("observer not set to snapshot service")
            return

        for i in range(count):
            fd = cv2.imread("./test-image.jpg")
            # Encode image to be sent as a message
            out, buf = cv2.imencode('.jpg', fd)

            self.observer.begin_notify(buf, "ISTI corridor camera", self.metadata)
            print("snapshot taken")

            time.sleep(delay)


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        properties = broker.getProperties()
        servant = SnapshotServiceI(properties)

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("snapshot-service"))

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
