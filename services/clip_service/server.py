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

    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        super(self.__class__, self).__init__()

    def notify(self, source, data, current=None):
        self.metadata = data
        self.trigger(self.properties.getProperty('ClipService.RecordTime'))

    def trigger(self, record_time, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        record = self.captureAudio(record_time)
        self.observer.begin_notify(record, 'ITSI-microphone', self.metadata)

    def capture_audio(self, record_time, current=None):
        # plughw is the sound card interface
        process = subprocess.Popen(['arecord -D plughw:2 --duration=%s -f cd ./test-images/record.wav' % record_time],
                                    shell = True, stdout=subprocess.PIPE)
        output, error = process.communicate()

        rate, samples = scipy.io.wavfile.read('./records/record.wav')

        # Convert audio as numpy array
        audio = np.asarray(samples, dtype=np.int16)
        return audio


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        properties = broker.getProperties()
        servant = ClipService(properties)

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("clip-service"))

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        
        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
