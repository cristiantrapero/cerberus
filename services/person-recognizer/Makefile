# -*- mode: makefile-gmake; coding: utf-8 -*-

DESTDIR           ?= ~
export PYTHONPATH  = src

all:

install:
	pip install scikit-learn
	pip2 install -r src/requirements.txt
	python src/setup.py install
	$(DESTDIR)/usr/lib/person-recognizer/models/get-models.sh
	install -d $(DESTDIR)/usr/bin
	install -m 744 person-recognizer $(DESTDIR)/usr/bin/
	install -d $(DESTDIR)/usr/lib/person-recognizer/
	install -m 644 src/server.py $(DESTDIR)/usr/lib/person-recognizer
	install -d $(DESTDIR)/usr/lib/person-recognizer/models
	install -m 644 models/* $(DESTDIR)/usr/lib/person-recognizer/models
	install -d $(DESTDIR)/etc/default
	install -m 644 src/server.config $(DESTDIR)/etc/default/person-recognizer.config
	

clean:
	$(RM) -rf ./test/__pycache__ ./src/__pycache__
