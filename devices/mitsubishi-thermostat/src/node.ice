// -*- mode: c++; coding: utf-8 -*-

#include <iot/node.ice>
#include <citisim/iot.ice>

module IoT {
    interface Node extends
        NodeAdmin,
        WiFiAdmin,
        SmartObject::DigitalSink {
    };
};
