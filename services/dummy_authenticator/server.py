#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
import Ice

CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/services.ice --all'.format(CITISIM_SLICE))
import SmartObject

class AuthenticatorI(SmartObject.AuthenticatedCommandService):
    def __init__(self):
        self.observer = None
        self.metadata = None
        self.personID = None
        self.command = None
        self.personAuthorized = ['MariaJose', 'David', 'Cristian','SteveCarell']
        self.commandAuthorized = ['abrir puerta', 'abrir', 'abreme', 'abrir la puerta', 'abreme la puerta', 'abre la puerta', 'abre']

    def setObserver(self, observer, current=None):
        ic = current.adapter.getCommunicator()
        self.observer = SmartObject.DigitalSinkPrx.checkedCast(ic.stringToProxy(observer))

    def notifyPerson(self, meta, personID, current=None):
        self.metadata = meta
        self.personID = personID

        authorizedPerson = self.findPersonInDB()
        if authorizedPerson == True:
            if self.command is not None:
                self.openDoor()

    def notifyCommand(self, meta, command, current=None):
        self.command = command

        authorizedPerson = self.findPersonInDB()
        if authorizedPerson == True:
            if self.personID is not None:
                self.openDoor()

    def findPersonInDB(self, current=None):
        if self.personID in self.personAuthorized:
            return True
        else:
            return False

    def openDoor(self, current=None):
        if any(x in self.command for x in self.commandAuthorized):
            self.observer.notify(True, self.metadata.source, self.metadata)
        else:
            self.observer.notify(False, self.metadata.source, self.metadata)

class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = AuthenticatorI()

        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("authenticator"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
