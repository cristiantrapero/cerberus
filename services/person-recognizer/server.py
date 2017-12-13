#!/usr/bin/python2 -u
# -*- coding: utf-8 -*-
import sys
import logging
import openface
import pickle
import numpy as np
import cv2
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

from sklearn.pipeline import Pipeline
from sklearn.lda import LDA
from sklearn.preprocessing import LabelEncoder
from sklearn.svm import SVC
from sklearn.grid_search import GridSearchCV
from sklearn.mixture import GMM
from sklearn.tree import DecisionTreeClassifier
from sklearn.naive_bayes import GaussianNB

MODEL_PREDICTIONFACE = './models/dlib/shape_predictor_68_face_landmarks.dat'
MODEL_TORCH = './models/openface/nn4.small2.v1.t7'

# Use the classifier of celebrities as example
CLASSIFIER_MODEL = './models/celeb-classifier.nn4.small2.v1.pkl'

class PersonRecognizerI(citisim.ObservableMixin, SmartObject.PersonRecognizer):
    observer_cast = SmartObject.AuthenticatedCommandServicePrx

    def __init__(self):
        self.metadata = None
        super(self.__class__, self).__init__()

    def trigger(self, data, meta, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        self.metadata = meta

        # Decode the data to read
        snapshot = cv2.imdecode(np.frombuffer(data, np.uint8), 1)

        # Get the id of the person
        person_id = self.recognize_person(snapshot)

        self.observer.notifyPerson(self.metadata, person_id)

    def recognize_person(self, data ,current=None):
        with open(CLASSIFIER_MODEL, 'rb') as f:
            if sys.version_info[0] < 3:
                (le, clf) = pickle.load(f)
            else:
                (le, clf) = pickle.load(f, encoding='latin1')

        # Use dlib’s landmark estimation to align faces
        align = openface.AlignDlib(MODEL_PREDICTIONFACE)

        # Get the largest face from the image
        bb = align.getLargestFaceBoundingBox(data)

        # Align the face from the image
        aligned_face = align.align(
            96, data, bb,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

        if aligned_face is None:
            logging.error("No face detected.\n")
            return

        net = openface.TorchNeuralNet(MODEL_TORCH, imgDim=96, cuda=False)

        rep = net.forward(aligned_face)
        repa = rep.reshape(1, -1)

        predictions = clf.predict_proba(repa).ravel()
        maxI = np.argmax(predictions)
        person = le.inverse_transform(maxI)
        confidence = predictions[maxI]
        person_id = person.decode('utf-8')

        if confidence > 0.60:
            print("Identified person: {} with {} confidence".format(person_id, confidence))
            return person_id
        else:
            print("Identified unknown: {} with {} confidence".format(person_id, confidence))
            person_id = "unknown"
            return person_id


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()

        try:
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        except Ice.InitializationException:
            logging.info("No config provided, using : '{}'".format(CONFIG_FILE))
            properties.setProperty('Ice.Config', CONFIG_FILE)
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")

        servant = PersonRecognizerI()
        proxy = adapter.add(servant, broker.stringToIdentity("person-recognizer"))

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


if __name__ == '__main__':
    try:
        sys.exit(Server().main(sys.argv))
    except SystemExit:
        sys.exit(1)
