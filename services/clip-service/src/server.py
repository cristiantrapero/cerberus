#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import subprocess
import scipy.io.wavfile
import numpy as np
import time
import os
import datetime
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
        self.soundcard = int(self.get_property('ClipService.SoundCard'))
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
            logging.error("The clip couldn't be sent. Observer not established.")
            return
        
        if recording is 1:
            logging.error("Audio record couldn't be sent.")
        else:
            self.observer.begin_notify(recording, self.place, self.metadata)
            logging.info("Audio record sent.")


    def capture_audio(self, seconds, current=None):
        # plughw is the sound card interface
        timestamp = time.time()
        date = datetime.datetime.fromtimestamp(timestamp)
        logging.info("Start recording at {}.".format(date))

        try:
            self.ring_buzzer()
            command = 'arecord -D plughw:{} --duration {} -f cd {}/record.wav'.format(self.soundcard, seconds, self.directory)
            os.system(command)
            self.ring_buzzer()
        except:
            logging.error("Unexpected error: {}".format(sys.exc_info()[0]))
            return 1

        try:
            rate, samples = scipy.io.wavfile.read('{}/record.wav'.format(self.directory))
            # Convert audio as numpy array
            audio = np.asarray(samples, dtype=np.int16)
            return audio
        except:
            logging.error("Unexpected error: {}".format(sys.exc_info()[0]))
            return 1


    def ring_buzzer(self, current=None):
        if os.uname()[1] == 'cerberus-rpi':
            os.system('gpio -g mode 22 out')
            os.system('gpio -g write 22 1')
            time.sleep(0.5)
            os.system('gpio -g write 22 0')


class Server(Ice.Application):
    def run(self, args):
        ice = self.communicator()
        properties = ice.getProperties()
        adapter = ice.createObjectAdapter("Adapter")
        adapter.activate()

        servant = ClipServiceI(properties)
        proxy = adapter.add(servant, ice.stringToIdentity("clip-service"))

        proxy = citisim.remove_private_endpoints(proxy)
        logging.info("Server ready: '{}'".format(proxy))

        self.shutdownOnInterrupt()
        ice.waitForShutdown()

        return 0


if __name__ == '__main__':
    try:
        sys.exit(Server().main(sys.argv))
    except SystemExit:
        sys.exit(1)
