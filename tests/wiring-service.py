#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import Ice

Ice.loadSlice('-I {0} {0}/citisim/wiring.ice --all'.format('/usr/share/slice'))
import SmartObject


class Client(Ice.Application):
    def run(self, args):
        proxy = self.communicator().stringToProxy(args[1])
        wiringPrx = SmartObject.WiringServicePrx.checkedCast(proxy)

        wiringPrx.addObserver("motion-sensor", "snapshot-service")
        print("snapshot-service set as consumer of motion-sensor")
        wiringPrx.addObserver("motion-sensor", "clip-service")
        print("clip-service set as consumer of motion-sensor")

sys.exit(Client().main(sys.argv))
