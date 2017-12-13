# -*- mode: makefile-gmake; coding: utf-8 -*-

DIRNAME = $(notdir $(shell 'pwd'))
DESTDIR?=~

all:

install:
	install -d $(DESTDIR)/usr/bin/
	install -m 744 motion-sensor $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/cerberus/motion-sensor/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/cerberus/motion-sensor/
	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/motion-sensor.config

clean:
	find . \( -name "*.pyc" -o -name "*~" \) -print -delete
