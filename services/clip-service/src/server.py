#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import subprocess
import scipy.io.wavfile
import numpy as np
import RPi as GPIO
import time
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.DEBUG)

CONFIG_FILE = 'src/server.config'

# RPI GPIO Buzzer configuration to sound when record audio
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(22,GPIO.OUT)

class ClipServiceI(citisim.ObservableMixin, SmartObject.ClipService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self, properties):
        self.metadata = None
        self.recordTime = int(properties.getProperty('ClipService.RecordTime'))
        self.place = str(properties.getProperty('ClipService.Place'))
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
        self.buzzer()
        # plughw is the sound card interface
        process = subprocess.Popen(['arecord -D plughw:0 --duration=%s -f cd /tmp/record.wav' % recordTime],
                                    shell=True, stdout=subprocess.PIPE)

        output, error = process.communicate()
        self.buzzer()

        rate, samples = scipy.io.wavfile.read('/tmp/record.wav')

        # Convert audio as numpy array
        audio = np.asarray(samples, dtype=np.int16)
        return audio

    def buzzer(self, current=None):
        GPIO.output(22, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(22, GPIO.LOW)
        time.sleep(0.1)
        GPIO.output(22, GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output(22, GPIO.LOW)


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

        servant = ClipServiceI(properties)
        proxy = adapter.add(servant, broker.stringToIdentity("clip-service"))

        proxy = citisim.remove_private_endpoints(proxy)
        logging.info("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    try:
        sys.exit(Server().main(sys.argv))
    except SystemExit:
        sys.exit(1)
