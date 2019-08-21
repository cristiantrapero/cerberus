#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import subprocess
import scipy.io.wavfile
import numpy as np
import time
import os
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.INFO)


class ClipServiceI(citisim.ObservableMixin, SmartObject.ClipService):
    observer_cast = SmartObject.DataSinkPrx

    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        self.seconds = int(self.get_property('ClipService.Seconds'))
        self.place = str(self.get_property('ClipService.Place'))
        self.directory = os.path.abspath(str(self.get_property('ClipService.Directory')))
        super(self.__class__, self).__init__()

    def get_property(self, key, default=None):
        retval = self.properties.getProperty(key)
        if retval is "":
            logging.info("Warning: property '{}' not set!".format(key))
            if default is not None:
                logging.info(" - using default value: {}".format(default))
                return default
            else:
                raise NameError("Ice property '{}' is not set".format(key))
        return retval

    def notify(self, eventName, source, data, current=None):
        self.metadata = data
        self.trigger(self.seconds)

    def trigger(self, seconds, current=None):
        recording = self.capture_audio(seconds)

        if not self.observer:
            logging.error("The clip couldn't be sent. Observer not set.")
            return
            
        self.observer.begin_notify(recording, self.place, self.metadata)

    def capture_audio(self, seconds, current=None):
        # plughw is the sound card interface
        self.ring_buzzer()
        subprocess.call(["arecord", "-D", "plughw:0", "--duration", str(seconds), "-f", "cd", "{}/record.wav".format(self.directory)])
        self.ring_buzzer()

        rate, samples = scipy.io.wavfile.read('{}/record.wav'.format(self.directory))

        # Convert audio as numpy array
        audio = np.asarray(samples, dtype=np.int16)
        return audio

    def ring_buzzer(self, current=None):
        if os.uname()[1] == 'cerberus-rpi':
            subprocess.call(['gpio -g mode 22 out'])
            subprocess.call(['gpio -g write 22 1'])
            time.sleep(0.5)
            subprocess.call(['gpio -g write 22 0'])


class Server(Ice.Application):
    def run(self, args):
        broker = self.communicator()
        properties = broker.getProperties()
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
