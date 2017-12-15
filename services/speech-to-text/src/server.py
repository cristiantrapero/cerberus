#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import json
import Ice
import logging
import scipy.io.wavfile
import numpy as np
from struct import *
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1

import libcitisim as citisim
from libcitisim import SmartObject

CONFIG_FILE="src/server.config"

class SpeechToTextI(SmartObject.SpeechToText):
    observer_cast = SmartObject.AuthenticatedCommandServicePrx

    def __init__(self, properties):
        self.metadata = None
        self.IBMusername = properties.getProperty("SpeechToText.IBMusername")
        self.IBMpassword = properties.getProperty("SpeechToText.IBMpassword")
        super(self.__class__, self).__init__()

    def notify(self, data, source, metadata, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        self.metadata = metadata
        command = self.speechToText(data)
        self.observer.notifyCommand(str(command), self.metadata)

    def speechToText(self, data):
        # Credentials IBM service
        speech_to_text = SpeechToTextV1(
            username = str(self.IBMusername),
            password = str(self.IBMpassword),
            x_watson_learning_opt_out = False
        )

        audio = np.fromstring(data, np.int16)

        # Convert numpy array as matrix [n/2, 2]
        audio = audio.reshape(audio.size//2, 2)

        # Write the audio data to send after
        scipy.io.wavfile.write('/tmp/command.wav', 44100, audio)

        with open(join(dirname(__file__), '/tmp/command.wav'),'rb') as audio_file:
            response = json.dumps(speech_to_text.recognize(
                audio_file, model = 'es-ES_BroadbandModel', content_type = 'audio/wav',
                word_confidence = True),
                indent = 2)
            loggin.info(response)

            response_data = json.loads(response)

            transcript = ""

            try:
                transcript = (response_data["results"][0]["alternatives"][0]["transcript"]).encode('utf-8')
            except:
                logging.error("Speech not detected")

            command = transcript.rstrip()

        return command


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        properties = broker.getProperties()

        try:
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        except Ice.InitializationException:
            logging.info("No config provided, using : '{}'".format(CONFIG_FILE))
            properties.setProperty('Ice.Config', CONFIG_FILE)
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")

        servant = SpeechToTextI(properties)
        proxy = adapter.add(servant, broker.stringToIdentity("speech-to-text"))

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
