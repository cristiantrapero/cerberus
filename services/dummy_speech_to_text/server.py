#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
import Ice

CITISIM_SLICE = '/usr/share/slice/citisim'
Ice.loadSlice('{}/services.ice --all'.format(CITISIM_SLICE))
import SmartObject

class SpeechToTextI(SmartObject.SpeechToText):
    def __init__(self):
        self.observer = None
        self.metadata = None

    def setObserver(self, observer, current=None):
        ic = current.adapter.getCommunicator()
        self.observer = SmartObject.AuthenticatedCommandServicePrx.checkedCast(ic.stringToProxy(observer))

    def trigger(self, meta, data, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        self.metadata = meta
        command = "abrir puerta"
        self.observer.notifyCommand(self.metadata, command)


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = SpeechToTextI()

        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("speech_to_text"))

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
