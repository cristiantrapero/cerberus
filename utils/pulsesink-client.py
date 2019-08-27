#!/usr/bin/python3 -u
# -*- mode: python; coding: utf-8 -*-

import sys
import Ice
from libcitisim import SmartObject


class Client(Ice.Application):
    def run(self, args):
        if len(args) != 2:
            print("Usage: <proxy>")
            return 1

        ic = self.communicator()
        door = ic.stringToProxy(args[1])
        door = door.ice_encodingVersion(Ice.Encoding_1_0)
        door = SmartObject.PulseSinkPrx.uncheckedCast(door)
        door.notify("DummyClient", {})
        print("notified!")

if __name__ == "__main__":
    Client().main(sys.argv)