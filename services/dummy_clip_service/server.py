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

    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        super(self.__class__, self).__init__()

    def notify(self, source, metadata, current=None):
        self.metadata = metadata
        self.trigger(self.properties.getProperty('ClipService.record_time'))

    def trigger(self, record_time, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        record = self.capture_audio(record_time)
        self.observer.begin_notify(record, 'microphone', self.metadata)

    def capture_audio(self, record_time):
        rate, samples = scipy.io.wavfile.read('./voice-command.wav')
        audio = np.asarray(samples, dtype=np.int16)
        return audio


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        properties = broker.getProperties()
        servant = ClipServiceI(properties)

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("clip-service"))

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
