#!/usr/bin/python -u
# -*- coding: utf-8 -*-
import sys
import time
import logging
import cv2
import requests
import json
import urllib
import os
import Ice
Ice.loadSlice('./slices/services.ice --all -I .')
import SmartObject

class SnapshotServiceI(SmartObject.SnapshotService):
    def __init__(self):
        self.observer = None
        self.metadata = None

    def setObserver(self, observer, current):
        proxy = current.adapter.getCommunicator().stringToProxy(observer)
        self.observer = SmartObject.DataSinkPrx.checkedCast(proxy)

    def notify(self, source, meta, position, current=None):
        self.metadata = meta[0]

        # Take 1 picture every 0 seconds
        self.trigger(1, 0)

    def trigger(self, count, deltaSeconds, current=None):
        if not self.observer:
            logging.error("observer not set")
            return

        for i in range(count):
            if self.getSnapshot == True:
                self.takeSnapshot()
                # Open image with OpenCV
                fd = cv2.imread("./test-images/snapshot.jpg")
            else:
                # Example image
                fd = cv2.imread("./test-images/carell.jpg")

            # Encode image to send as message
            out, buf = cv2.imencode('.jpg', fd)

            # Send the image
            self.observer.trigger(self.metadata, buf)
            time.sleep(deltaSeconds)

    def takeSnapshot(self, current=None):
        # Reference in the API: https://developers.nest.com/documentation/cloud/api-camera#snapshot_url
        url = "https://developer-api.nest.com/devices/cameras/OFuOPQq5W6mRdufVJknqvIrfQNoI5joS0-MjWTb9H5KkFvCyiy_EuQ/snapshot_url"

        token = "c.T7xUsJZKNj8RNJ7ryrMBQe02WejukQldrIv2YoR9HMkgB5UPSKbQpkF9PDkXOUy3rPjiXep8ZCL0QK12mYPr5KpIfAYMk907tzfATBqljxUd23aNDM0yM4VaVN6deM3mtfEoj2v3eHUHjpde" # Update with your token

        headers = {'Authorization': 'Bearer {0}'.format(token), 'Content-Type': 'application/json'} # Update with your token

        initial_response = requests.get(url, headers=headers, allow_redirects=False)
        if initial_response.status_code == 307:
            initial_response = requests.get(initial_response.headers['Location'], headers=headers, allow_redirects=False)

        # Get the snapshot url
        urlSnapshot = initial_response.text.strip('\'"')

        # Get and write the snapshot in disk
        urllib.urlretrieve(urlSnapshot, "./test-images/snapshot.jpg")


class Server(Ice.Application):
    def run(self, argv):
        broker = self.communicator()
        servant = SnapshotServiceI()

        adapter = broker.createObjectAdapter("Adapter")
        proxy = adapter.add(servant, broker.stringToIdentity("snapshot_service"))

        sys.stdout.flush()

        adapter.activate()
        self.shutdownOnInterrupt()
        broker.waitForShutdown()

        return 0


sys.exit(Server().main(sys.argv))
