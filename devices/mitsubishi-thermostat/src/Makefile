# -*- mode: makefile-gmake; coding: utf-8 -*-

SLICE_DIR  = /usr/share/slice
SLICES     = node.ice

all: $(SLICES:%.ice=%.h)

%.h: %.ice
	slice2c -I $(SLICE_DIR) --ice $^


.PHONY: clean
clean:
	$(RM) $(SLICES:%.ice=%.h)
