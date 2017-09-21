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

    def __init__(self):
        self.metadata = None
        super().__init__()

    def notify(self, source, data, current=None):
        self.metadata = data

        # Take 1 picture every 0 seconds
        self.trigger(1, 0)

    def trigger(self, count, delta_seconds, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        for i in range(count):
            fd = cv2.imread("./test-image.jpg")

            # Encode image to send as message
            out, buf = cv2.imencode('.jpg', fd)

            self.observer.trigger(self.metadata, buf)
            time.sleep(delta_seconds)


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = SnapshotServiceI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.addWithUUID(servant)

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
