#!/usr/bin/python3
# -*- coding: utf-8; mode: python; tab-width:4 -*-
import sys
import os

import Ice
from unittest import TestCase

import scheduler

class SchedulerTests(TestCase):
    def setUp(self):
        props = Ice.createProperties([])
        props.setProperty('Ice.Default.Locator',
                          'IceGrid/Locator -t:tcp -h 127.0.0.1 -p 4061')
        init_data = Ice.InitializationData()
        init_data.properties = props
        ic = Ice.initialize(init_data)
        
        self.sut = scheduler.Scheduler(ic)

    def test_get_action(self):
        result = self.sut.get_action_for_event('motion detected')
        self.assertEquals(result, '{detect_motion}')
        
    def test_motion_detected(self):
        result = self.sut.make_schedule('motion detected')
        self.assertEquals(result, ['motion-sensor'])

    def test_motion_detected(self):
        result = self.sut.make_schedule('scene snapshoted')
        self.assertEquals(result, ['motion-sensor', 'snapshot-service'])




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
