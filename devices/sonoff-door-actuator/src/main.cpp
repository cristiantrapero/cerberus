// -*- mode: cpp; coding: utf-8 -*-

#include <Arduino.h>
#include <Ticker.h>

#include <ArduinoOTA.h>    // force IDE to include this
#include <ESP8266WiFi.h>   // force IDE to include this
#include <ESP8266mDNS.h>   // force IDE to include this
#include <EEPROM.h>        // force IDE to include this

#include <IceC.h>
#include <IceC/platforms/esp8266/TCPEndpoint.h>
#include <IceC/platforms/esp8266/debug.hpp>
#include <IceC-IoT-node.h>

#include "iot-node.h"
#include "iot.h"

#define RELAY_PIN 12

// IceC broker and adapter
Ice_Communicator ic;
Ice_ObjectAdapter adapter;

// servants
IoT_IoTNode node;
SmartObject_EventSink relay;

void
IoT_NodeAdminI_restart(IoT_NodeAdminPtr self) {
    async_restart_node();
}

void
IoT_NodeAdminI_factoryReset(IoT_NodeAdminPtr self) {
    async_factory_reset();
}

void
IoT_WiFiAdminI_setupWiFi(IoT_WiFiAdminPtr self,
                         Ice_String ssid,
                         Ice_String key) {
    store_wifi_settings(ssid, key);
}

void
SmartObject_EventSinkI_notify(SmartObject_EventSinkPtr self,
                              Ice_String source,
                              SmartObject_Metadata data) {
    Serial.println("EventSink: notify");
    digitalWrite(RELAY_PIN, HIGH);
    async.once(1, []() {
        digitalWrite(RELAY_PIN, LOW);
    });
}

void setup() {
    Serial.begin(115200);
    Serial.flush();
    pinMode(STATUS_LED, OUTPUT);
    pinMode(RELAY_PIN, OUTPUT);
    delay(100);
    Serial.println("\n------\nBooting...\n");

    // setup WiFi, Ice, Endpoints...
    IceC_Storage_begin();
    setup_wireless();
    setup_ota();
    Ice_initialize(&ic);
    TCPEndpoint_init(&ic);

    // setup adapter and register servants
    Ice_Communicator_createObjectAdapterWithEndpoints
        (&ic, "Adapter", "tcp -p 4455", &adapter);
    Ice_ObjectAdapter_activate(&adapter);
    IoT_IoTNode_init(&node);
    SmartObject_EventSink_init(&relay);

    // FIXME: add interface to set these identities
    Ice_ObjectAdapter_add(&adapter, (Ice_ObjectPtr)&node, "Node");
    Ice_ObjectAdapter_add(&adapter, (Ice_ObjectPtr)&relay, "Door");

    Serial.println("Boot done!\n");
}

void loop() {
    handle_ota();
    check_buttons();
    Ice_Communicator_loopIteration(&ic);
}
