#!/usr/bin/python3 -u
# -*- mode: python; coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice("../../../slice/iot.ice")
import SmartObject  # noqa


class Client(Ice.Application):
    def run(self, args):
        ic = self.communicator()

        if len(args) != 2:
            print("Usage: {} <proxy>".format(args[0]))
            return 1

        door = ic.stringToProxy(args[1])
        door = door.ice_encodingVersion(Ice.Encoding_1_0)
        door = SmartObject.EventSinkPrx.uncheckedCast(door)

        door.notify("Client", {})


if __name__ == "__main__":
    Client().main(sys.argv)
