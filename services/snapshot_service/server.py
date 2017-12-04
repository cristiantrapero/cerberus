#!/usr/bin/python2 -u
# -*- coding: utf-8 -*-
import sys
import time
import logging
import cv2
import urllib
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class SnapshotServiceI(citisim.ObservableMixin, SmartObject.SnapshotService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self):
        self.metadata = None
        super(self.__class__, self).__init__()

    def notify(self, source, data, current=None):
        self.metadata = data

        self.trigger(Ice.getProperty('SnapshotService.NumSnapshots'),
                     Ice.getProperty('SnapshotService.TimeToShot'))

    def trigger(self, count, delta_seconds, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        for i in range(count):
            self.take_snapshot()
            fd = cv2.imread("./snapshots/snapshot.jpg")

            # Encode image to send as message
            out, buf = cv2.imencode('.jpg', fd)

            self.observer.trigger(self.metadata, buf)
            time.sleep(delta_seconds)

    def take_snapshot(self, current=None):
        url_snapshot = "http://{}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={}&pwd={}".format(Ice.getProperty('SnapshotService.IPCamera'),
                                                                                               Ice.getProperty('SnapshotService.CameraUSER'),
                                                                                               Ice.getProperty('SnapshotService.CameraPASS'))
        urllib.urlretrieve(url_snapshot, "./snapshots/snapshot.jpg")


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = SnapshotServiceI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("snapshot-service"))

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
