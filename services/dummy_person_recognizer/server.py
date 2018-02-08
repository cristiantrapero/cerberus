#!/usr/bin/python2 -u
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
        super(self.__class__, self).__init__()

    def notify(self, data, source, metadata, current=None):
        self.metadata = metadata

        # Decode the data to read
        snapshot = cv2.imdecode(np.frombuffer(data, np.uint8), 1)

        # Get the id of the person
        personID = self.recognize_person(snapshot)

        self.observer.begin_notifyPerson(personID, self.metadata)

    def recognize_person(self, snapshot, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        personID = "SteveCarell"
        return personID


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = PersonRecognizerI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("person-recognizer"))

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0

    
sys.exit(Server().main(sys.argv))
