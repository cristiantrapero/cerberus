#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
import logging
import numpy as np
import cv2
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class PersonRecognizerI(citisim.ObservableMixin, SmartObject.PersonRecognizer):
    observer_cast = SmartObject.AuthenticatedCommandServicePrx

    def __init__(self):
        self.metadata = None
        super().__init__()

    def trigger(self, meta, data, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        self.metadata = meta

        # Decode the data to read
        face = cv2.imdecode(np.frombuffer(data, np.uint8), 1)

        # Get the id of the person
        personID = self.recognize_person(face)

        self.observer.notifyPerson(self.metadata, personID)

    def recognize_person(self, data, current=None):
        personID = "SteveCarell"
        return personID


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = PersonRecognizerI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.addWithUUID(servant)

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
