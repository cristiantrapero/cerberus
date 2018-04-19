#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import json
import scipy.io.wavfile
import numpy as np
from os.path import join, dirname
from watson_developer_cloud import SpeechToTextV1
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.INFO)


class SpeechToTextI(citisim.ObservableMixin, SmartObject.SpeechToText):
    observer_cast = SmartObject.AuthenticatedCommandServicePrx

    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        self.IBMusername = str(self.get_property("SpeechToText.IBMusername"))
        self.IBMpassword = str(self.get_property("SpeechToText.IBMpassword"))
        self.directory = str(self.get_property("SpeechToText.Directory"))
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

    def notify(self, data, source, metadata, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        self.metadata = metadata
        transcription = self.transcribeAudio(data)
        self.observer.notifyCommand(transcription, self.metadata)
        print("message '{}' sent".format(transcription))

    def transcribe_audio(self, data):
        # Credentials IBM service
        speech_to_text = SpeechToTextV1(
            username=self.IBMusername,
            password=self.IBMpassword,
            url='https://stream.watsonplatform.net/speech-to-text/api'
        )

        audio = np.fromstring(data, np.int16)

        # Convert numpy array as matrix [n/2, 2]
        audio = audio.reshape(audio.size//2, 2)

        # Write the audio data to send after
        scipy.io.wavfile.write('/tmp/command.wav', 44100, audio)

        with open(join(dirname(__file__), '/tmp/command.wav'), 'rb') as audio_file:
            response = json.dumps(speech_to_text.recognize(
                audio_file, model='es-ES_BroadbandModel', content_type='audio/wav',
                word_confidence=True),
                indent=2)

            response_data = json.loads(response)

            transcript = ""

            try:
                transcript = (response_data["results"][0]["alternatives"][0]["transcript"]).encode('utf-8')
            except:
                logging.error("Speech not detected")

            command = str(transcript.rstrip())

        return command


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        properties = broker.getProperties()
        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")

        servant = SpeechToTextI(properties)
        proxy = adapter.add(servant, broker.stringToIdentity("speech-to-text"))

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
