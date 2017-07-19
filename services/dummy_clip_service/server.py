#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
import time
import logging
import scipy.io.wavfile
import numpy as np
import Ice

CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/services.ice --all'.format(CITISIM_SLICE))
import SmartObject

class ClipServiceI(SmartObject.ClipService):
    def __init__(self):
        self.observer = None
        self.metadata = None

    def setObserver(self, observer, current=None):
        ic = current.adapter.getCommunicator()
        self.observer = SmartObject.DataSinkPrx.checkedCast(ic.stringToProxy(observer))

    def notify(self, source, data, current=None):
        self.metadata = data

        # Capture sound for 10 seconds
        self.trigger(10)

    def trigger(self, duration_seconds, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        record = self.captureAudio(duration_seconds)

        self.observer.trigger(self.metadata, record)

    def captureAudio(self, duration_seconds, current=None):
        rate, samples = scipy.io.wavfile.read('./commandVoice.wav')
        audio = np.asarray(samples, dtype=np.int16)
        return audio


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ClipServiceI()

        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("clip_service"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
