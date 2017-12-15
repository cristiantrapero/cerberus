# -*- mode: makefile-gmake; coding: utf-8 -*-

DESTDIR           ?= ~
export PYTHONPATH  = src

all:

install:
	pip3 install watson-developer-cloud scipy
	install -d $(DESTDIR)/usr/bin
	install -m 744 speech-to-text $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/speech-to-text/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/speech-to-text
	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/speech-to-text.config

clean:
	$(RM) -rf ./test/__pycache__ ./src/__pycache__
