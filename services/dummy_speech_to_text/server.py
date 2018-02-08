#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import Ice
import logging

import libcitisim as citisim
from libcitisim import SmartObject


class SpeechToTextI(citisim.ObservableMixin, SmartObject.SpeechToText):
    observer_cast = SmartObject.AuthenticatedCommandServicePrx

    def __init__(self):
        self.metadata = None
        super(self.__class__, self).__init__()

    def notify(self, data, source, metadata, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        self.metadata = metadata
        transcription = self.speechToText(data)
        self.observer.begin_notifyCommand(transcription, self.metadata)

    def speechToText(self, audio):
        transcription = "abreme la puerta"
        return transcription


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = SpeechToTextI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("speech-to-text"))

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
