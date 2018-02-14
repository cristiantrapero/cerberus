#!/usr/bin/python2 -u
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
        self.trigger(self.properties.getProperty('SnapshotService.Snapshots'),
                     self.properties.getProperty('SnapshotService.Delay'))

    def trigger(self, count, delay, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        for i in range(int(count)):
            fd = cv2.imread("./test-image.jpg")

            # Encode image to send as message
            out, buf = cv2.imencode('.jpg', fd)

            self.observer.begin_notify(buf, "ISTI-camera", self.metadata)
            time.sleep(int(delay))


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        logger = broker.getLogger()
        logger.trace("info", "snapshot service started")
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
