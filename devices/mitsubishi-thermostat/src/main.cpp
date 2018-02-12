// -*- mode: cpp; coding: utf-8 -*-

#include <Arduino.h>

#include <ArduinoOTA.h>    // force IDE to include this
#include <ESP8266WiFi.h>   // force IDE to include this
// #include <ESP8266mDNS.h>   // force IDE to include this
// #include <EEPROM.h>        // force IDE to include this

#include <IceC.h>
#include <IceC/platforms/esp8266/TCPEndpoint.h>
#include <IceC/platforms/esp8266/debug.hpp>
#include <IceC-IoT-node.h>

#include "node.h"

// IceC broker and adapter
Ice_Communicator ic;
Ice_ObjectAdapter adapter;

// servants
IoT_Node node;

// pin configuration
#define PIN_STATUS    14    // thermostat on or off
#define PIN_POWER     13
#define PIN_TEMP_UP   4
#define PIN_TEMP_DOWN 5

void
setup_pins() {
    pinMode(PIN_STATUS, INPUT);
    pinMode(PIN_POWER, OUTPUT);
    pinMode(PIN_TEMP_UP, OUTPUT);
    pinMode(PIN_TEMP_DOWN, OUTPUT);
    pinMode(LED_BUILTIN, OUTPUT);
}

void
blink(byte count, byte delay_ms) {
    for (byte i=0; i<count; i++) {
        digitalWrite(LED_BUILTIN, LOW);
        delay(50);
        digitalWrite(LED_BUILTIN, HIGH);
        delay(delay_ms);
    }
}

void
button_press(byte button) {
    digitalWrite(button, HIGH);
    delay(200);
    digitalWrite(button, LOW);
}

void
IoT_NodeAdminI_restart(IoT_NodeAdminPtr self) {
    async_restart_node();
    blink(3, 50);    
}

void
IoT_NodeAdminI_factoryReset(IoT_NodeAdminPtr self) {
    async_factory_reset();
    blink(3, 50);
}

void
IoT_WiFiAdminI_setupWiFi(IoT_WiFiAdminPtr self,
                         Ice_String ssid,
                         Ice_String key) {
    store_wifi_settings(ssid, key);
    blink(3, 50);
}

void
SmartObject_DigitalSinkI_notify(SmartObject_DigitalSinkPtr self,
                                Ice_Bool value,
                                Ice_String source,
                                SmartObject_Metadata data) {

    // status has an inverted logic
    bool status = !digitalRead(PIN_STATUS);

    if (value != status)
        button_press(PIN_POWER);
    blink(3, 50);
}

void setup() {
    Serial.begin(115200);
    Serial.flush();
    setup_pins();
    blink(3, 200);

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
    IoT_Node_init(&node);

    // FIXME: add interface to set these identities
    Ice_ObjectAdapter_add(&adapter, (Ice_ObjectPtr)&node, "Node");

    Serial.println("Boot done!\n");
    blink(1, 50);
}

void loop() {
    handle_ota();
    check_buttons();
    Ice_Communicator_loopIteration(&ic);
}
