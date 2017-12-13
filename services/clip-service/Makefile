# -*- mode: makefile-gmake; coding: utf-8 -*-

DIRNAME = $(notdir $(shell 'pwd'))
DESTDIR?=~

all:

install:
	install -d $(DESTDIR)/usr/bin/
	install -m 744 clip-service $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/cerberus/clip-service/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/cerberus/clip-service/
	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/clip-service.config

clean:
	find . \( -name "*.pyc" -o -name "*~" \) -print -delete
