// -*- coding: utf-8; mode: c++; tab-width:4 -*-

#include "iot.ice"

module Private {
  interface MotionService extends SmartObject::EventSink, SmartObject::Observable {};
};
