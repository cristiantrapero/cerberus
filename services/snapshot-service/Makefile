# -*- mode: makefile-gmake; coding: utf-8 -*-

DESTDIR           ?= ~
export PYTHONPATH  = src

all:

install:
	install -d $(DESTDIR)/usr/bin
	install -m 744 snapshot-service $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/snapshot-service/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/snapshot-service
	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/snapshot-service.config

clean:
	$(RM) -rf ./test/__pycache__ ./src/__pycache__
