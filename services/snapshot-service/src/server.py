#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import os
import logging
import cv2
import urllib.request
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.INFO)


class SnapshotServiceI(citisim.ObservableMixin, SmartObject.SnapshotService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        self.snapshots = int(self.get_property('SnapshotService.Snapshots'))
        self.delay = int(self.get_property('SnapshotService.Delay'))
        self.place = str(self.get_property('SnapshotService.Place'))
        self.cameraIP = str(self.get_property('SnapshotService.CameraIP'))
        self.cameraUser = str(self.get_property('SnapshotService.CameraUser'))
        self.cameraPass = str(self.get_property('SnapshotService.CameraPass'))
        self.directory = os.path.abspath(str(self.get_property('SnapshotService.Directory')))
        super(self.__class__, self).__init__()

    def get_property(self, key, default=None):
        retval = self.properties.getProperty(key)
        if retval is "":
            logging.info("Warning: property '{}' not set!".format(key))
            if default is not None:
                logging.info(" - using default value: {}".format(default))
                return default
            else:
                raise NameError("You must add the property '{}'".format(key))
        return retval

    def notify(self, source, metadata, current=None):
        self.metadata = metadata
        self.trigger(self.snapshots, self.delay)

    def trigger(self, snapshots, delay, current=None):
        for i in range(snapshots):
            
            try:
                url_snapshot = "http://{}:88/cgi-bin/CGIProxy.fcgi?cmd=snapPicture2&usr={}&pwd={}".format(self.cameraIP, self.cameraUser, self.cameraPass)
                urllib.request.urlretrieve(url_snapshot, "{}/snapshot.jpg".format(self.directory))
            except urllib.error.URLError:
                logging.error("IP Camera URL error. Check the IP, user and camera pass.\n")
                return

            try:
                fd = cv2.imread("{}/snapshot.jpg".format(self.directory))
                # Encode image to send as message
                out, buf = cv2.imencode('.jpg', fd)
            except cv2.error:
                logging.error("The JPEG image is empty or not created.")
                return 

            if not self.observer:
                logging.error("The image couldn't be sent. Observer not set to snapshot service.")
                return

            self.observer.begin_notify(buf, self.place, self.metadata)
            logging.info("Snapshot taken.")

            time.sleep(delay)        


class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        properties = broker.getProperties()
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
