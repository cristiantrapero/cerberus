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

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.DEBUG)

CONFIG_FILE = 'src/server.config'


class SnapshotServiceI(citisim.ObservableMixin, SmartObject.SnapshotService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self, properties):
        self.metadata = None
        self.snapshots = int(properties.getProperty('SnapshotService.Snapshots'))
        self.delay = int(properties.getProperty('SnapshotService.Delay'))
        self.place = str(properties.getProperty('SnapshotService.Place'))
        self.cameraIP = str(properties.getProperty('SnapshotService.CameraIP'))
        self.cameraUser = str(properties.getProperty('SnapshotService.CameraUser'))
        self.cameraPass = str(properties.getProperty('SnapshotService.CameraPass'))
        super(self.__class__, self).__init__()

    def notify(self, source, metadata, current=None):
        self.metadata = metadata
        self.trigger(self.snapshots, self.delay)

    def trigger(self, snapshots, delay, current=None):
        if not self.observer:
            logging.error("observer not set to snapshot service")
            return

        for i in range(snapshots):
            self.take_snapshot()
            fd = cv2.imread("/tmp/cerberus/snapshot.jpg")

            # Encode image to send as message
            out, buf = cv2.imencode('.jpg', fd)

            self.observer.begin_notify(buf, self.place, self.metadata, buf)
            print("snapshot taken")

            time.sleep(delay)

    def take_snapshot(self, current=None):
        url_snapshot = "http://{}:88/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={}&pwd={}".format(self.cameraIP, self.CameraUser, self.cameraPass)
        urllib.urlretrieve(url_snapshot, "/tmp/cerberus/snapshot.jpg")


class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        properties = broker.getProperties()

        try:
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        except Ice.InitializationException:
            logging.info("No config provided, using : '{}'".format(CONFIG_FILE))
            properties.setProperty('Ice.Config', CONFIG_FILE)
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")

        servant = SnapshotServiceI(properties)
        proxy = adapter.add(servant, broker.stringToIdentity("snapshot-service"))

        proxy = citisim.remove_private_endpoints(proxy)
        logging.info("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    try:
        sys.exit(Server().main(sys.argv))
    except SystemExit:
        sys.exit(1)
