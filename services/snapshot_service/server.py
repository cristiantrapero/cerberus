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

        for i in range(count):
            self.take_snapshot()
            fd = cv2.imread("./snapshots/snapshot.jpg")

            # Encode image to send as message
            out, buf = cv2.imencode('.jpg', fd)

            self.observer.begin_notify(buf, "ITSI-camera", self.metadata, buf)
            time.sleep(delay)

    def take_snapshot(self, current=None):
        url_snapshot = "http://{}/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={}&pwd={}".format(
                          self.properties.getProperty('SnapshotService.CameraIP'),
                          self.properties.getProperty('SnapshotService.CameraUser'),
                          self.properties.getProperty('SnapshotService.CameraPass'))
        urllib.urlretrieve(url_snapshot, "./snapshots/snapshot.jpg")


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


sys.exit(Server().main(sys.argv))
