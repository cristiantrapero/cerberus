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
        motion = self.communicator().stringToProxy("motion-sensor")

        if not motion:
            raise RuntimeError('Invalid proxy')

        motion.ice_ping()
        print("ice_ping to: {}".format(motion))
        return 0


sys.exit(Cliente().main(sys.argv))
