#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import logging
import Ice

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

import libcitisim as citisim
from libcitisim import SmartObject

CONFIG_FILE = 'src/Server.config'


class EventHandler(PatternMatchingEventHandler):
    patterns = ["*.jpg", "*.png"]

    def __init__(self, servant):
        super(EventHandler, self).__init__(ignore_patterns=["*.png~"])
        self.servant = servant

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        self.servant.notify()


class ObservableI(citisim.ObservableMixin, SmartObject.Observable):
    observer_cast = SmartObject.EventSinkPrx

    def __init__(self, properties):
        self.latitude = properties.getProperty('MotionSensor.Latitude')
        self.longitude = properties.getProperty('MotionSensor.Longitude')
        self.altitude = properties.getProperty('MotionSensor.Altitude')
        self.place = properties.getProperty('MotionSensor.Place')
        super(self.__class__, self).__init__()

    def notify(self):
        if not self.observer:
            logging.error("observer not set")
            return

        data = citisim.MetadataHelper(
            timestamp = time.time(),
            quality = 255,
            expiration = 30,
            latitude = 38.99793,
            longitude = -3.919898,
            altitude = 637.10,
            place = self.place).to_dict()

        self.observer.begin_notify(self.place, data)


class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()

        properties = broker.getProperties()
        servant = ObservableI(properties)

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("motion-sensor"))

        print(properties.getProperty('MotionSensor.MonitoredDirectory'))
        # monitor = Observer()
        # monitor.schedule(EventHandler(servant), str(properties.getProperty('MotionSensor.MonitoredDirectory')))
        # monitor.start()

        proxy = citisim.remove_private_endpoints(proxy)
        logging.info("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


if __name__ == '__main__':
    try:
        sys.exit(Server().main(sys.argv))
    except SystemExit:
        sys.exit(1)
