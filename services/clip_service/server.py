#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import subprocess
import scipy.io.wavfile
import numpy as np
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class ClipService(citisim.ObservableMixin, SmartObject.ClipService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self):
        self.metadata = None
        super().__init__()

    def notify(self, source, data, current=None):
        self.metadata = data

        # Capture sound for 5 seconds
        self.trigger(Ice.getProperty('ClipService.TimeToRecord'))

    def trigger(self, duration_seconds, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        record = self.captureAudio(duration_seconds)

        self.observer.trigger(record, 'put-sender-identity-here', self.metadata)

    def capture_audio(self, duration_seconds, current=None):
        # plughw is the sound card interface
        process = subprocess.Popen(['arecord -D plughw:2 --duration=%s -f cd ./test-images/record.wav' % duration_seconds], shell = True, stdout=subprocess.PIPE)
        output, error = process.communicate()

        rate, samples = scipy.io.wavfile.read('./records/record.wav')

        # Convert audio as numpy array
        audio = np.asarray(samples, dtype=np.int16)
        return audio


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = ClipService()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("clip-service"))

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
