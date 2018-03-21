#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import numpy as np
import scipy.io.wavfile
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class ClipServiceI(citisim.ObservableMixin, SmartObject.ClipService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self, properties):
        self.metadata = None
        self.recordTime = int(properties.getProperty('ClipService.RecordTime'))
        super(self.__class__, self).__init__()

    def notify(self, source, metadata, current=None):
        self.metadata = metadata
        self.trigger(self.recordTime)

    def trigger(self, recordTime, current=None):
        if not self.observer:
            logging.error("observer not set to clip service")
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
