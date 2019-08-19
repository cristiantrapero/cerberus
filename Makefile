#!/usr/bin/make -f
# -*- mode:makefile -*-

NODES=$(notdir $(basename $(shell ls config/node*.config | sort -r)))
NODE_DIRS=$(addprefix /tmp/cerberus/db/, $(NODES))
IG_ADMIN=icegridadmin --Ice.Config=config/locator.config -u user -p pass
APP=Dummy Access Control Service

define GRID_STOP
    @if ss -lptn 2> /dev/null | grep ":4061" > /dev/null; then \
	for node in $(NODES); do \
            $(IG_ADMIN) -e "node shutdown $$node"; \
	done; \
	killall icegridnode; \
	echo -- grid stop ok; \
    fi
endef

define WAIT_READY
    @while ! $(IG_ADMIN) -e "node list" 2> /dev/null | grep "node1" > /dev/null; do \
	echo -- waiting registry ready; \
        sleep 1; \
    done
endef

define APP_RM
    $(call WAIT_READY)
    @if $(IG_ADMIN) -e "application remove '$1'" > /dev/null 2>&1; then \
        echo -- app \"$1\" removed ok; \
    fi
endef

grid-restart: grid-stop grid-start

grid-start: /tmp/cerberus/db/registry $(NODE_DIRS) /tmp/cerberus/db/icestorm
	icegridnode --Ice.Config=config/node1.config &
	$(call WAIT_READY)
	@echo -- grid start ok

grid-stop:
	$(call GRID_STOP)

app-add: app-rm
	$(call WAIT_READY)
	$(IG_ADMIN) -e "application add config/cerberus-dummy-app.xml"
	@echo -- app \"$(APP)\" added ok;

test-app-add: app-rm
	$(call WAIT_READY)
	$(IG_ADMIN) -e "application add deploy/cerberus-test-app.xml"
	@echo -- app \"$(APP)\" added ok;

app-rm:
	$(call APP_RM,$(APP))

start-services:
	@for server in $(shell $(IG_ADMIN) -e "server list"); do \
	   $(IG_ADMIN) -e "server start $$server"; \
	   echo "$$server started"; \
	done

show-nodes:
	$(IG_ADMIN) -e "node list"

run-scheduler:
	./scheduler/scheduler.py --Ice.Config=config/locator.config scone WiringServer

simulate-motion:
	./utils/simulate-motion.py --Ice.Config=config/locator.config

run-test-wiring-service:
	./tests/wiring-service.py --Ice.Config=config/locator.config WiringService

connect-authenticator-to-sonoff:
	./utils/set-observer.py --Ice.Config=config/locator.config "authenticator" "Door -t -e 1.1:tcp -h 161.67.106.89 -p 4455"

restart: clean grid-start app-add

install-dependencies:
	bash -c "./install-dependencies.sh"

/tmp/cerberus/%:
	mkdir -p $@

clean:
	$(call GRID_STOP)
	-$(RM) *~
	-$(RM) -r .scone
	-$(RM) -r /tmp/cerberus
	@echo -- clean ok
