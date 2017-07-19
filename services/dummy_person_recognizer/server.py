#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
import logging
import numpy as np
import cv2
import Ice

CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/services.ice --all'.format(CITISIM_SLICE))
import SmartObject


class PersonRecognizerI(SmartObject.PersonRecognizer):
    def __init__(self):
        self.observer = None
        self.metadata = None

    def setObserver(self, observer, current):
        ic = current.adapter.getCommunicator()
        self.observer = SmartObject.AuthenticatedCommandServicePrx.checkedCast(ic.stringToProxy(observer))

    def trigger(self, meta, data, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        self.metadata = meta

        # Decode the data to read
        face = cv2.imdecode(np.frombuffer(data, np.uint8), 1)

        # Get the id of the person
        personID = recognize_person(face)

        self.observer.notifyPerson(self.metadata, personID)

    def recognize_person(self, data ,current=None):
        personID = "SteveCarell"
        return personID

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = PersonRecognizerI()

        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("person_recognizer"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
