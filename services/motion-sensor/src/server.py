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

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.DEBUG)

CONFIG_FILE = 'src/server.config'


class Handler(PatternMatchingEventHandler):
    patterns = ["*.jpg", "*.png"]

    def __init__(self, servant):
        super(Handler, self).__init__(ignore_patterns=["*.png~"])
        self.servant = servant

    def on_created(self, event):
        self.process(event)

    def process(self, event):
        self.servant.notify()


class MotionSensorI(citisim.ObservableMixin, SmartObject.Observable):
    observer_cast = SmartObject.EventSinkPrx

    def __init__(self, properties):
        self.quality = int(properties.getProperty('MotionSensor.Quality'))
        self.expiration = int(properties.getProperty('MotionSensor.Expiration'))
        self.latitude = float(properties.getProperty('MotionSensor.Latitude'))
        self.longitude = float(properties.getProperty('MotionSensor.Longitude'))
        self.altitude = float(properties.getProperty('MotionSensor.Altitude'))
        self.place = str(properties.getProperty('MotionSensor.Place'))
        super(self.__class__, self).__init__()

    def notify(self, current=None):
        if not self.observer:
            logging.error("observer not set to motion sensor")
            return

        data = citisim.MetadataHelper(
            timestamp=time.time(),
            quality=self.quality,
            expiration=self.expiration,
            latitude=self.latitude,
            longitude=self.longitude,
            altitude=self.altitude,
            place=self.place).to_dict()

        self.observer.begin_notify(self.place, data)
        logging.info('motion detected on {}'.format(self.place))


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

        servant = MotionSensorI(properties)
        proxy = adapter.add(servant, broker.stringToIdentity("motion-sensor"))

        # Matches given patterns with file paths associated with occurring events.
        monitor = Observer()
        monitoredDirectory = str(properties.getProperty('MotionSensor.MonitoredDirectory'))
        monitor.schedule(Handler(servant), monitoredDirectory)

        try:
            monitor.start()
        except OSError:
            logging.error("MonitoredDirectory property is not a directory.")
            return 1

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
