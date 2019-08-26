#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import cv2
import sys
import logging
import numpy as np
import openface
import pickle
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.INFO)


class PersonRecognizerI(citisim.ObservableMixin, SmartObject.PersonRecognizer):
    observer_cast = SmartObject.AuthenticatedCommandServicePrx

    def __init__(self, properties):
        self.metadata = None
        self.properties = properties
        self.classifier_model = str(self.get_property('PersonRecognizer.ClassifierModel', './models/openface/celeb-classifier.nn4.small2.v1.pkl'))
        self.predictionface_model = str(self.get_property('PersonRecognizer.PredictionFaceModel', './models/dlib/shape_predictor_68_face_landmarks.dat'))
        self.torch_model = str(self.get_property('PersonRecognizer.TorchModel', './models/openface/nn4.small2.v1.t7'))
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
            logging.error("Observer not established")
            return

        self.metadata = metadata

        # Decode the data to read
        snapshot = cv2.imdecode(np.frombuffer(data, np.uint8), 1)

        # Get the id of the person
        person_id = self.recognize_person(snapshot)
        self.observer.begin_notifyPerson(person_id, self.metadata)
        logging.info("Identified person as {}".format(person_id))

    def recognize_person(self, data, current=None):
        with open(self.classifier_model, 'rb') as f:
            if sys.version_info[0] < 3:
                (le, clf) = pickle.load(f)
            else:
                (le, clf) = pickle.load(f, encoding='latin1')

        # Use dlib’s landmark estimation to align faces
        align = openface.AlignDlib(self.predictionface_model)

        # Get the largest face from the image
        bb = align.getLargestFaceBoundingBox(data)

        # Align the face from the image
        aligned_face = align.align(
            96, data, bb,
            landmarkIndices=openface.AlignDlib.OUTER_EYES_AND_NOSE)

        if aligned_face is None:
            logging.info("No face detected.\n")
            return None

        net = openface.TorchNeuralNet(self.torch_model, imgDim=96, cuda=False)

        rep = net.forward(aligned_face)
        repa = rep.reshape(1, -1)

        predictions = clf.predict_proba(repa).ravel()
        maxI = np.argmax(predictions)
        person = le.inverse_transform(maxI)
        confidence = predictions[maxI]
        person_id = person.decode('utf-8')

        if confidence > 0.60:
            logging.info("Identified person {} with {} confidence.".format(person_id, confidence))
            return person_id
        else:
            logging.info("Unknown person. Estimated: {} with {} confidence.".format(person_id, confidence))
            person_id = "unknown"
            return person_id


class Server(Ice.Application):
    def run(self, argv):
        ice = self.communicator()
        adapter = ice.createObjectAdapter("Adapter")
        properties = ice.getProperties()
        adapter.activate()

        servant = PersonRecognizerI(properties)
        proxy = adapter.add(servant, ice.stringToIdentity("person-recognizer"))

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
