#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import time
import sys
import logging
import Ice

import libcitisim as citisim
from libcitisim import SmartObject
mkey = SmartObject.MetadataField


class MotionSensorI(citisim.ObservableMixin, SmartObject.Observable):
    observer_cast = SmartObject.EventSinkPrx

    def ice_ping(self, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        metadata = citisim.MetadataHelper(
            timestamp = 10,
            quality = 200,
            expiration = 10,
            latitude = 38.99793,
            longitude = 3.919898,
            altitude = 637.10,
            place = 'ITSI').to_dict()

        self.observer.begin_notify('ITSI', metadata)


class MotionSensor(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        logger = broker.getLogger()
        logger.trace("info", "motion sensor started")
        servant = MotionSensorI()

        adapter = broker.createObjectAdapterWithEndpoints('Adapter', 'tcp')
        proxy = adapter.add(servant, broker.stringToIdentity("motion-sensor"))

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(MotionSensor().main(sys.argv))
