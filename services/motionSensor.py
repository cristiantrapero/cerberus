#!/usr/bin/python -u
# -*- coding: utf-8 -*-

import sys
import time
import Ice
Ice.loadSlice('./slices/services.ice --all -I .')
import SmartObject

class MotionSensor(Ice.Application):
    def run(self, argv):
        inicio = time.time()
        # Get camera proxy
        file_camera = open("./proxy-out/camera.out", "r")
        proxy_camera = self.communicator().stringToProxy(file_camera.readline())
        camera = SmartObject.EventSinkPrx.checkedCast(proxy_camera)
        file_camera.close()

        # Get microphone proxy
        file_microphone = open("./proxy-out/microphone.out", "r")
        proxy_microphone = self.communicator().stringToProxy(file_microphone.readline())
        microphone = SmartObject.EventSinkPrx.checkedCast(proxy_microphone)
        file_microphone.close()

        metadata = [SmartObject.MeasureMetadata(int(time.time()), 255, 30)]
        position = [SmartObject.Position(38.997932, -3.919898, 637.10, "studio-door")]

        # Notify motion
        microphone.notify("motion-sensor", metadata, position)
        camera.notify("motion-sensor", metadata, position)

        print("Motion detected in the studio door.\n")
        print("Tiempo de ejecucion: {}".format(time.time()-inicio))
        return 0


sys.exit(MotionSensor().main(sys.argv))
