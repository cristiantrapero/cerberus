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

class SpeechToTextI(SmartObject.SpeechToText):
    observer_cast = SmartObject.AuthenticatedCommandServicePrx

    def trigger(self, data, meta, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        self.metadata = meta
        command = self.speechToText(data)
        self.observer.notifyCommand(str(command), self.metadata)

    def speechToText(self, data):
        # Credentials IBM service
        speech_to_text = SpeechToTextV1(
            username = 'ef4417e7-cb37-4898-a457-2a8d9f255d89',
            password = 'ETRMgWLYmtKj',
            x_watson_learning_opt_out = False
        )

        audio = np.fromstring(data, np.int16)

        # Convert numpy array as matrix [n/2, 2]
        audio = audio.reshape(audio.size//2, 2)

        # Write the audio data to send after
        scipy.io.wavfile.write('./commands/command.wav', 44100, audio)

        with open(join(dirname(__file__), './commands/command.wav'),
                  'rb') as audio_file:
            response = json.dumps(speech_to_text.recognize(
                audio_file, model='es-ES_BroadbandModel',content_type='audio/wav',
                word_confidence=True),
                indent=2)
            print(response)

            response_data = json.loads(response)

            transcript = ""

            try:
                transcript = (response_data["results"][0]["alternatives"][0]["transcript"]).encode('utf-8')
            except:
                logging.error("Speech not detected")

            command = transcript.rstrip()

        return transcript


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = SpeechToTextI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("speech-to-text"))

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
