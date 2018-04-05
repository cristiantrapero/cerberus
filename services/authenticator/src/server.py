#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import Ice
import logging

import libcitisim as citisim
from libcitisim import SmartObject
from libcitisim import MetadataField

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.DEBUG)

CONFIG_FILE = "src/server.config"


class AuthenticatorI(citisim.ObservableMixin, SmartObject.Observable):
    observer_cast = SmartObject.EventSinkPrx

    def __init__(self):
        self.metadata_personID = None
        self.metadata_command = None
        self.personID = None
        self.command = None
        self.person_authorized = ['Cristian', 'SteveCarell']
        self.command_authorized = ['abrir puerta', 'abrir', 'abreme', 'abrir la puerta', 'abreme la puerta', 'abre la puerta', 'abre']
        super(self.__class__, self).__init__()

    def notifyPerson(self, personID, metadata, current=None):
        self.metadata_personID = metadata
        self.personID = personID
        self.checkAuthorization()

    def notifyCommand(self, command, metadata, current=None):
        self.metadata_command = metadata
        self.command = command
        self.checkAuthorization()

    def checkAuthorization(self, current=None):
        if not self.observer:
            logging.error("observer not set to authenticator service")
            return

        # If we have a command and a person identification
        if self.command is not None and self.personID is not None:
            if self.personID in self.person_authorized:

                if any(x in self.command for x in self.command_authorized):
                    placeCommand = self.metadata_command.get(MetadataField.Place)
                    placePersonID = self.metadata_personID.get(MetadataField.Place)

                    # Events generated in the same place
                    if placeCommand == placePersonID:
                        self.observer.begin_notify(placeCommand, self.metadata_personID)
                        logging.info("{} authorized to {}".format(self.personID, self.command))

                        # Clean
                        self.command = None
                        self.personID = None
            else:
                logging.info("{} is not authorized person".format(self.personID))


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        properties = broker.getProperties()

        try:
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        except Ice.InitializationException:
            logging.info("No config provided, using : '{}'".format(CONFIG_FILE))
            properties.setProperty('Ice.Config', CONFIG_FILE)
            adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")

        servant = AuthenticatorI()
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
