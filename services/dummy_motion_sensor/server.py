#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice

import libcitisim as citisim
from libcitisim import SmartObject
mkey = SmartObject.MetadataField


class ObservableI(SmartObject.Observable):
    def __init__(self):
        self.observer = None

    def setObserver(self, observer, current=None):
        ic = current.adapter.getCommunicator()
        proxy = ic.stringToProxy(observer)
        self.observer = SmartObject.EventSinkPrx.checkedCast(proxy)

    def ping(self, current=None):
        if not self.observer:
            print("Observer not set!")
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
        proxy = adapter.addWithUUID(servant)

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(MotionSensor().main(sys.argv))
