#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
import sys
import Ice

import libcitisim as citisim
from libcitisim import SmartObject
mkey = SmartObject.MetadataField

class AuthenticatorI(citisim.ObservableMixin, SmartObject.Observable):
    observer_cast = SmartObject.EventSinkPrx

    def __init__(self):
        self.metadata_person = None
        self.metadata_command = None
        self.id_person = None
        self.command = None
        self.person_authorized = ['MariaJose', 'David', 'Cristian', 'SteveCarell']
        self.command_authorized = ['abrir puerta', 'abrir', 'abreme', 'abrir la puerta', 'abreme la puerta', 'abre la puerta', 'abre']
        super().__init__()

    def notifyPerson(self, meta, id_person, current=None):
        self.metadata_person = meta
        self.id_person = id_person
        self.checkAuthorization()

    def notifyCommand(self, meta, command, current=None):
        self.metadata_command = meta
        self.command = command
        self.checkAuthorization()

    def checkAuthorization(self, current=None):
        if self.id_person in self.person_authorized:
            if any(x in self.command for x in self.command_authorized):
                if self.metadata_person.source == self.metadata_command.source:
                    self.observer.notify(True, self.metadata_command.source, self.metadata_command)

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = AuthenticatorI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.addWithUUID(servant)

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
