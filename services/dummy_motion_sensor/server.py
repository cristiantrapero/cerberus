#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import logging
import Ice

import libcitisim as citisim
from libcitisim import SmartObject
mkey = SmartObject.MetadataField


class ObservableI(citisim.ObservableMixin, SmartObject.Observable):
    observer_cast = SmartObject.EventSinkPrx

    def ping(self, current=None):
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

        adapter = broker.createObjectAdapterWithEndpoints('Adapter', 'tcp')
        proxy = adapter.add(servant, broker.stringToIdentity("motion-sensor"))

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(MotionSensor().main(sys.argv))
