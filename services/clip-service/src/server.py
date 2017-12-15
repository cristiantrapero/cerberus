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

CONFIG_FILE = 'src/server.config'


class ClipService(citisim.ObservableMixin, SmartObject.ClipService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self, properties):
        self.metadata = None
        self.recordTime = properties.getProperty('ClipService.RecordTime')
        self.place = properties.getProperty('ClipService.Place')
        super(self.__class__, self).__init__()

    def notify(self, source, data, current=None):
        self.metadata = data
        self.trigger(self.recordTime)

    def trigger(self, recordTime, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        record = self.captureAudio(recordTime)
        self.observer.begin_notify(record, self.place, self.metadata)

    def capture_audio(self, recordTime, current=None):
        # plughw is the sound card interface
        process = subprocess.Popen(['arecord -D plughw:0 --duration=%s -f cd /tmp/record.wav' % recordTime],
                                    shell = True, stdout=subprocess.PIPE)
        output, error = process.communicate()

        rate, samples = scipy.io.wavfile.read('/tmp/record.wav')

        # Convert audio as numpy array
        audio = np.asarray(samples, dtype=np.int16)
        return audio


class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        properties = broker.getProperties()

        try:
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        except Ice.InitializationException:
            logging.info("No config provided, using : '{}'".format(CONFIG_FILE))
            properties.setProperty('Ice.Config', CONFIG_FILE)
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")

        servant = ClipService(properties)
        proxy = adapter.add(servant, broker.stringToIdentity("clip-service"))

        proxy = citisim.remove_private_endpoints(proxy)
        loggin.info("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    try:
        sys.exit(Server().main(sys.argv))
    except SystemExit:
        sys.exit(1)
