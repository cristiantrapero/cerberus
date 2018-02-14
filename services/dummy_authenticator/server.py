#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import Ice

import libcitisim as citisim
from libcitisim import SmartObject


class AuthenticatorI(citisim.ObservableMixin, SmartObject.AuthenticatedCommandService):
    observer_cast = SmartObject.EventSinkPrx

    def __init__(self):
        self.metadata_personID = None
        self.metadata_command = None
        self.personID = None
        self.command = None
        self.person_authorized = ['MariaJose', 'David', 'Cristian', 'SteveCarell']
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
                if self.metadata_personID.get('Place') == self.metadata_command.get('Place'):
                    if not self.observer:
                        logging.error("observer not set")
                        return

                    self.observer.begin_notify(self.metadata_personID.get('Place'), self.metadata_personID)
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
