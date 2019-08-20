#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import json
import scipy.io.wavfile
import numpy as np
from os.path import join, dirname, abspath
from watson_developer_cloud import SpeechToTextV1
from watson_developer_cloud.websocket import RecognizeCallback
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
        self.APIKey = str(self.get_property("SpeechToText.APIKey"))
        self.URL = str(self.get_property("SpeechToText.URL"))
        self.directory = abspath(str(self.get_property("SpeechToText.Directory")))
        super(self.__class__, self).__init__()

    def get_property(self, key, default=None):
        retval = self.properties.getProperty(key)
        if retval is "":
            logging.info("Warning: property '{}' not set!".format(key))
            if default is not None:
                logging.info(" - using default value: {}".format(default))
                return default
            else:
                raise NameError("You must add the property '{}'".format(key))
        return retval

    def notify(self, data, source, metadata, current=None):
        self.metadata = metadata
        transcription = self.transcribe_audio(data)
        
        if not self.observer:
            logging.error("observer not set")
            return

        self.observer.begin_notifyCommand(transcription, self.metadata)
        logging.info("message '{}' sent".format(transcription))

    def transcribe_audio(self, data):
        # Credentials IBM service
        speech_to_text = SpeechToTextV1(
            iam_apikey=self.APIKey,
            url=self.URL)

        audio = np.fromstring(data, np.int16)

        # Convert numpy array as matrix [n/2, 2]
        audio = audio.reshape(audio.size//2, 2)

        # Write the audio data to send after
        scipy.io.wavfile.write('{}/command.wav'.format(self.directory), 44100, audio)

        with open(join(dirname(__file__), '{}/command.wav'.format(self.directory)), 'rb') as audio_file:
            try:
                response = json.dumps(speech_to_text.recognize(
                    audio=audio_file,
                    content_type='audio/wav',
                    model='es-ES_BroadbandModel').get_result(),
                    indent=2, ensure_ascii=False)
            except TypeError as err:
                logging.info(err)
                return

            try:
                transcript = json.loads(response)["results"][0]["alternatives"][0]["transcript"]
            except:
                logging.info("Speech not detected.")
                return None
            return transcript


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
