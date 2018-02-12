# -*- mode: makefile-gmake; coding: utf-8 -*-

SLICE_DIR  = /usr/share/slice
SLICES     = iot-node.ice iot.ice

vpath %.ice ../lib/IceC-IoT-node/slice
vpath %.ice ../../../slice

all: $(SLICES:%.ice=%.h)

%.h: %.ice
	slice2c -I $(SLICE_DIR)/iot $^

.PHONY: clean
clean:
	$(RM) $(SLICES:%.ice=%.h)
