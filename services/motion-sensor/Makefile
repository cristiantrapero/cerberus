# -*- mode: makefile-gmake; coding: utf-8 -*-

DESTDIR           ?= ~
export PYTHONPATH  = src

all:

install:
	pip3 install watchdog
	install -d $(DESTDIR)/usr/bin
	install -m 744 motion-sensor $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/motion-sensor/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/motion-sensor
	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/motion-sensor.config

clean:
	$(RM) -rf ./test/__pycache__ ./src/__pycache__
