#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-
"usage: ./{} <observable-proxy> <observer-proxy>"

import sys
import logging
import Ice

import libcitisim as citisim
from libcitisim import SmartObject

class Client(Ice.Application):
    def run(self, args):
        if len(args) != 3:
            print(usage, args[0])
            return 1

        observable = self.communicator().stringToProxy(args[1])
        observable = SmartObject.ObservablePrx.uncheckedCast(observable)
        observer_str = args[2]

        if not observable:
            raise RuntimeError('Invalid proxy for observable')

        observable.setObserver(observer_str)
        return 0


sys.exit(Client().main(sys.argv))
