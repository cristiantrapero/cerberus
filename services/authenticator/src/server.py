#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import apiai
import csv
import Ice
import json
import logging
import sys

import libcitisim as citisim
from libcitisim import MetadataField
from libcitisim import SmartObject

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.INFO)


class AuthenticatorI(citisim.ObservableMixin, SmartObject.AuthenticatedCommandService):
    observer_cast = SmartObject.EventSinkPrx

    def __init__(self, properties):
        self.properties = properties
        self.metadata_personID = None
        self.metadata_command = None
        self.personID = None
        self.command = None
        self.database = str(self.get_property('Authenticator.Database', './authorized_people.csv'))
        self.dialogflow_token = str(self.get_property('Authenticator.DialogflowToken'))
        self.authorized_people = self.get_authorized_people(self.database)
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

    def notifyPerson(self, personID, metadata, current=None):
        self.metadata_personID = metadata
        self.personID = personID
        logging.info("Person: {}".format(self.personID))
        self.check_authorization()

    def notifyCommand(self, command, metadata, current=None):
        self.metadata_command = metadata
        if command != "":
            self.command = self.get_intention(command)
        logging.info("Command: {}".format(self.command))
        self.check_authorization()

    def check_authorization(self, current=None):
        # If we have a command and a person identification
        if self.command is not None and self.personID is not None:
            if not self.observer:
                logging.error("observer not set to authenticator service")
                return

            if self.personID in self.authorized_people.keys():
                if self.command in self.authorized_people.get(self.personID):
                    if self.metadata_command.get(MetadataField.Place) == self.metadata_personID.get(MetadataField.Place):
                        self.observer.begin_notify("authorized person", self.metadata_personID.get(MetadataField.Place), self.metadata_personID)
                        logging.info("{} authorized to: {}".format(self.personID, self.command))
                        self.clean_variables()
            else:
                logging.error("{} is not authorized person".format(self.personID))
                self.clean_variables()

    def get_intention(self, command, current=None):
        ai = apiai.ApiAI(self.dialogflow_token)

        request = ai.text_request()
        request.lang = 'es'
        request.query = command

        response = json.loads(request.getresponse().read().decode('utf-8'))
        message = response['result']['metadata']['intentName']
        return message

    def get_authorized_people(self, database, current=None):
        authorized_people = {}

        with open(database, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            for row in reader:
                authorized_people[row[0]] = row[1:]

        return authorized_people

    def clean_variables(self, current=None):
        self.metadata_personID = None
        self.metadata_command = None
        self.personID = None
        self.command = None


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        properties = broker.getProperties()
        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")

        servant = AuthenticatorI(properties)
        proxy = adapter.add(servant, broker.stringToIdentity("authenticator"))

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
