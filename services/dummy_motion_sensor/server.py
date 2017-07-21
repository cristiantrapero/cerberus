#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import time
import Ice

CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/iot.ice --all'.format(CITISIM_SLICE))
import SmartObject
from SmartObject import MetadataField as mkey


class ObservableI(SmartObject.Observable):
    def __init__(self):
        self.observer = None

    def setObserver(self, observer, current=None):
        ic = current.adapter.getCommunicator()
        self.observer = SmartObject.EventSinkPrx.checkedCast(ic.stringToProxy(observer))

    def detect_motion(self):
        # FIXME: migrate to libcitisim
        data = {
            mkey.Timestamp:  str(time.time()),
            mkey.Quality:    '255',
            mkey.Expiration: '30',
            mkey.Latitude:   '38.997932',
            mkey.Longitude:  '-3.919898',
            mkey.Altitude:   '637.10',
            mkey.Place:      'ITSI ARCO lab'
        }

        self.observer.notify("ITSI ARCO lab", data)


class MotionSensor(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ObservableI()

        adapter = broker.createObjectAdapter("Adapter")
        adapter.add(servant, broker.stringToIdentity("motion_sensor"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(MotionSensor().main(sys.argv))
