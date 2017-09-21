#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import Ice
import logging

import libcitisim as citisim
from libcitisim import SmartObject


class SpeechToTextI(citisim.ObservableMixin, SmartObject.SpeechToText):
    observer_cast = SmartObject.AuthenticatedCommandServicePrx

    def trigger(self, data, meta, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        command = "abrir puerta"
        self.observer.notifyCommand(command, meta)


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = SpeechToTextI()

        adapter = broker.createObjectAdapterWithEndpoints("Adapter", "tcp")
        proxy = adapter.addWithUUID(servant)

        adapter.activate()
        self.shutdownOnInterrupt()

        proxy = citisim.remove_private_endpoints(proxy)
        print("Server ready:\n'{}'".format(proxy))
        broker.waitForShutdown()


sys.exit(Server().main(sys.argv))
