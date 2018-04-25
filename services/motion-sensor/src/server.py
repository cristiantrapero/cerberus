#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import Ice
import logging
import os
import sys
import time

import libcitisim as citisim
from libcitisim import SmartObject

from watchdog.events import PatternMatchingEventHandler
from watchdog.observers import Observer

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.INFO)


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
        self.properties = properties
        self.quality = int(self.get_property('MotionSensor.Quality'))
        self.expiration = int(self.get_property('MotionSensor.Expiration'))
        self.latitude = float(self.get_property('MotionSensor.Latitude'))
        self.longitude = float(self.get_property('MotionSensor.Longitude'))
        self.altitude = float(self.get_property('MotionSensor.Altitude'))
        self.place = str(self.get_property('MotionSensor.Place'))
        super(self.__class__, self).__init__()

    def get_property(self, key, default=None):
        retval = self.properties.getProperty(key)
        if retval is "":
            logging.info("Warning: property '{}' not set!".format(key))
            if default is not None:
                logging.info(" - using default value: {}".format(default))
                return default
            else:
                raise NameError("Ice property '{}' is not set".format(key))
        return retval

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
        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")

        servant = MotionSensorI(properties)
        proxy = adapter.add(servant, broker.stringToIdentity("motion-sensor"))

        # Matches given patterns with file paths associated with occurring events.
        monitor = Observer()
        directory = str(properties.getProperty('MotionSensor.MonitoredDirectory'))

        if directory is "":
            logging.error("Error: property MonitoredDirectory not set!")
            return 1

        directory = os.path.abspath(directory)
        monitor.schedule(Handler(servant), directory)

        try:
            monitor.start()
        except OSError:
            logging.error("MonitoredDirectory property is not correct directory.")
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
