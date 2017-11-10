#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import logging
import Ice

import libcitisim as citisim
from libcitisim import SmartObject
mkey = SmartObject.MetadataField

class Cliente(Ice.Application):
    def run(self, argv):
        proxy = self.communicator().stringToProxy("motion-sensor")
        motion = SmartObject.ObservablePrx.uncheckedCast(proxy)

        if not motion:
            raise RuntimeError('Invalid proxy')

        print("Proxy: {} ".format(motion))

        motion.ice_ping()

        return 0


sys.exit(Cliente().main(sys.argv))
