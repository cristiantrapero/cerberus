#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import scipy.io.wavfile
import numpy as np
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class ClipServiceI(citisim.ObservableMixin, SmartObject.ClipService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self):
        self.metadata = None
        super().__init__()

    def notify(self, source, data, current=None):
        self.metadata = data

        # Capture sound for 10 seconds
        self.trigger(Ice.getProperty('ClipService.TimeToRecord'))

    def trigger(self, duration_seconds, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        record = self.capture_audio(duration_seconds)
        self.observer.trigger(record, 'put-sender-identity-here', self.metadata)

    def capture_audio(self, duration_seconds):
        rate, samples = scipy.io.wavfile.read('./voice-command.wav')
        audio = np.asarray(samples, dtype=np.int16)
        return audio


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ClipServiceI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("clip-service"))

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
