# -*- mode: makefile-gmake; coding: utf-8 -*-

DESTDIR           ?= ~
export PYTHONPATH  = src

all:

install:
	pip3 install scipy
	install -d $(DESTDIR)/usr/bin
	install -m 744 clip-service $(DESTDIR)/usr/bin/

	install -d $(DESTDIR)/usr/lib/clip-service/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/clip-service

	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/clip-service.config

clean:
	$(RM) -rf ./test/__pycache__ ./src/__pycache__
