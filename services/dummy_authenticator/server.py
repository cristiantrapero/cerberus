#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import logging
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

from SmartObject import MetadataField

class AuthenticatorI(citisim.ObservableMixin, SmartObject.AuthenticatedCommandService):
    observer_cast = SmartObject.EventSinkPrx

    def __init__(self):
        self.metadata_personID = None
        self.metadata_command = None
        self.personID = None
        self.command = None
        self.person_authorized = ['SteveCarell', 'Cristian']
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

        if self.command is not None and self.personID is not None:
            if self.personID in self.person_authorized:
                if any(x in self.command for x in self.command_authorized):
                    placeCommand = self.metadata_command.get(MetadataField.Place)
                    placePersonID = self.metadata_personID.get(MetadataField.Place)
                    if placeCommand == placePersonID:
                        self.observer.begin_notify(placeCommand, self.metadata_personID)
                        print("{} authorized to {}".format(self.personID, self.command))
                        self.command = None
                        self.personID = None
            else:
                print("{} is not authorized person".format(self.personID))

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = AuthenticatorI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.add(servant, broker.stringToIdentity("authenticator"))

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
