#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import Ice

CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/iot.ice --all'.format(CITISIM_SLICE))
import SmartObject


class ObservableI(SmartObject.Observable):
    def __init__(self):
        self.observer = None

    def setObserver(self, observer, current=None):
        ic = current.adapter.getCommunicator()
        self.observer = SmartObject.EventSinkPrx.checkedCast(ic.stringToProxy(observer))

    def detect_motion(self):
        data = {
            'timestamp':  str(time.time()),
            'quality':    '255',
            'expiration': '30',
            'latitude':   '38.997932',
            'longitude':  '-3.919898',
            'altitude':   '637.10',
            'place':      'ITSI ARCO lab'
        }

        self.observer.notify("ITSI ARCO lab", data)


class MotionSensor(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ObservableI()

        adapter = broker.createObjectAdapter("Adapter")
        adapter.add(servant, broker.stringToIdentity("actuator"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(MotionSensor().main(sys.argv))
