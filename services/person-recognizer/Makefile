# -*- mode: makefile-gmake; coding: utf-8 -*-

DESTDIR           ?= ~
export PYTHONPATH  = src

all:

install:
	install -d $(DESTDIR)/usr/bin
	install -m 744 person-recognizer $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/person-recognizer/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/person-recognizer
	install -d $(DESTDIR)/usr/lib/person-recognizer/models
	install -m 644 src/models/get-models.sh $(DESTDIR)/usr/lib/person-recognizer/models
	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/person-recognizer.config

clean:
	$(RM) -rf ./test/__pycache__ ./src/__pycache__
