#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import logging
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

CONFIG_FILE = 'src/server.config'


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
        self.quality = properties.getProperty('MotionSensor.Quality')
        self.expiration = properties.getProperty('MotionSensor.Expiration')
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
            quality = self.quality,
            expiration = self.expiration,
            latitude = self.latitude,
            longitude = self.longitude,
            altitude = self.altitude,
            place = self.place).to_dict()

        self.observer.begin_notify(self.place, data)


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

        servant = ObservableI(properties)
        proxy = adapter.add(servant, broker.stringToIdentity("motion-sensor"))

        monitor = Observer()
        monitor.schedule(EventHandler(servant), str(properties.getProperty('MotionSensor.MonitoredDirectory')))
        monitor.start()

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
