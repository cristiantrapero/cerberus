#!/usr/bin/python3 -u
# -*- coding: utf-8 -*-

import sys
import logging
import Ice

import libcitisim as citisim
from libcitisim import SmartObject
mkey = SmartObject.MetadataField

class Client(Ice.Application):
    def run(self, args):
        if len(args) == 2:
            strproxy = args[1]
        else:
            strproxy = 'motion-sensor'

        motion = self.communicator().stringToProxy(strproxy)

        if not motion:
            raise RuntimeError('Invalid proxy')

        motion.ice_ping()
        print("ice_ping to: {}".format(motion))
        return 0


sys.exit(Client().main(sys.argv))
