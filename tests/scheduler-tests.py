#!/usr/bin/python3
# -*- coding: utf-8; mode: python; tab-width:4 -*-
import sys
import os
if __name__ == '__main__' and __package__ is None:
    sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../scheduler')))

import scheduler
import Ice
from unittest import TestCase
from doublex import (
    assert_that, called, method_returning, method_raising, Mimic, Spy
)

class SchedulerTests(TestCase):
    def test_get_existing_service(self):
        return 0


# get plan for existing service:    event "recorded audio"
# get plan for trivial composition: event "voice command"
# get plan for non existing service: "lights service"
# get plan for non existing event: "turn on lights"
# get plan for non existing capability: "wav audio format"
# get plan for an action that could be perform by two services: "person recognition"
# get plan for existing service that have not proxy
# get plan for a service that requires two events that could be perform by two or more servies
# get plan for a service that has two subevents: "authenticator"
# get plan for a service that have not an instance
