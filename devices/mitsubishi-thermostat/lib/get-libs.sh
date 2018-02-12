#!/bin/bash
# -*- mode: sh; coding: utf-8 -*-

BB=https://bitbucket.org/arco_group

echo -n "IceC... "
if [ ! -d IceC ]; then
    wget -q $BB/icec/downloads/arduino-icec-latest.zip
    unzip -qq arduino-icec-latest.zip -d IceC
    rm arduino-icec-latest.zip
    echo "[ok] "
else
    echo "[already present]"
fi

echo -n "IceC-IoT-Node... "
if [ ! -d IceC-IoT-Node ]; then
    wget -q https://bitbucket.org/arco_group/iot.node/downloads/icec-iot-node-latest.zip
    unzip -qq icec-iot-node-latest.zip -d IceC-IoT-Node
    rm icec-iot-node-latest.zip
    echo "[ok] "
else
    echo "[already present]"
fi
