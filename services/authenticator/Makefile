# -*- mode: makefile-gmake; coding: utf-8 -*-

DESTDIR           ?= ~
export PYTHONPATH  = src

all:

install:
	install -d $(DESTDIR)/usr/bin/
	install -m 744 authenticator $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/authenticator/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/authenticator/
	install -m 644 src/authorized_people.csv $(DESTDIR)/usr/lib/authenticator/
	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/authenticator.config

clean:
	$(RM) -rf ./test/__pycache__ ./src/__pycache__
