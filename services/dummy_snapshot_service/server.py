#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
import time
import logging
import cv2
import Ice

CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/services.ice --all'.format(CITISIM_SLICE))
import SmartObject

class SnapshotServiceI(SmartObject.SnapshotService):
    def __init__(self):
        self.observer = None
        self.metadata = None

    def setObserver(self, observer, current):
        ic = current.adapter.getCommunicator()
        self.observer = SmartObject.DataSinkPrx.checkedCast(ic.stringToProxy(observer))

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

        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("snapshot_service"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
