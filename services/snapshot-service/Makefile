# -*- mode: makefile-gmake; coding: utf-8 -*-

DIRNAME = $(notdir $(shell 'pwd'))
DESTDIR?=~

all:

install:
	install -d $(DESTDIR)/usr/bin/
	install -m 744 snapshot-service $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/cerberus/snapshot-service/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/cerberus/snapshot-service/
	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/snapshot-service.config

clean:
	find . \( -name "*.pyc" -o -name "*~" \) -print -delete
