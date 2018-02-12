#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import Ice
import logging

import libcitisim as citisim
from libcitisim import SmartObject

stderrLogger = logging.StreamHandler()
stderrLogger.setFormatter(logging.Formatter(logging.BASIC_FORMAT))
logging.getLogger().addHandler(stderrLogger)
logging.getLogger().setLevel(logging.DEBUG)

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
        if self.personID in self.person_authorized:
            if any(x in self.command for x in self.command_authorized):
                if self.metadata_personID.place == self.metadata_command.place:
                    self.observer.begin_notify(self.metadata_personID.place, self.metadata_personID)
        else:
            logging.info("No authorized person")

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()

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
