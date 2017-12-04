#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import os
import sys
import time
import logging
import datetime
import Ice

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import libcitisim as citisim
from libcitisim import SmartObject
mkey = SmartObject.MetadataField


class MyHandler(PatternMatchingEventHandler):
    patterns = ["*.jpg", "*.png"]
    def __init__(self, servant):
        super(MyHandler, self).__init__(ignore_patterns=["*.png~"])
        self.servant = servant

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        self.servant.notify_movement()


class ObservableI(citisim.ObservableMixin, SmartObject.Observable):
    observer_cast = SmartObject.EventSinkPrx

    def notify_movement(self):
        if not self.observer:
            logging.error("observer not set")
            return

        data = citisim.MetadataHelper(
            timestamp = 'now',
            quality = 255,
            expiration = 30,
            latitude = 38.99793,
            longitude = -3.919898,
            altitude = 637.10,
            place = 'ITSI ARCO lab').to_dict()

        self.observer.notify("ITSI ARCO lab", data)


class MotionSensor(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ObservableI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("motion-sensor"))

        # Observing a directory changes
        observer = Observer()
        # observer.schedule(MyHandler(servant),Ice.getProperty('MotionSensor.CameraDirectory'))
        observer.schedule(MyHandler(servant), '/home/cristian/')
        observer.start()

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(MotionSensor().main(sys.argv))
