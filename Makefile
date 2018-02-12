#!/usr/bin/make -f
# -*- mode:makefile -*-

NODES=$(notdir $(basename $(shell ls config/node*.config | sort -r)))
NODE_DIRS=$(addprefix /tmp/db/, $(NODES))
IG_ADMIN=icegridadmin --Ice.Config=config/locator.config -u user -p pass

start-grid: /tmp/db/registry $(NODE_DIRS) /tmp/db/is.db 
	icegridnode --Ice.Config=config/node1.config &
	@while ! netstat -lptn 2> /dev/null | grep ":4061" > /dev/null; do \
	    sleep 1; \
	done
	@echo -- ok

stop-grid: 
	@for node in $(NODES); do \
	    $(IG_ADMIN) -e "node shutdown $$node"; \
	done

	@killall icegridnode
	@echo -- ok

app-rm:
	$(IG_ADMIN) -e "application remove 'Access Control System Prototipe'"

deploy:
	$(IG_ADMIN) -e "application add config/dummy-app.xml"
	$(IG_ADMIN) -e "server list"
	@echo -- app added

start-services: 
	@for server in $(shell $(IG_ADMIN) -e "server list"); do \
	   $(IG_ADMIN) -e "server start $$server"; \
	   echo "$$server started"; \
	done

show-nodes:
	$(IG_ADMIN) -e "node list"

run-scheduler:
	./scheduler/scheduler.py --Ice.Config=config/locator.config scone WiringService

simulate-motion:
	./services/simulate_motion/simulate-motion.py --Ice.Config=config/locator.config

restart: clean start-grid deploy

setup: start-services run-scheduler simulate-motion

/tmp/db/%:
	mkdir -p $@

clean: 
	-$(RM) *~
	-$(RM) -r ../.scone
	-$(RM) -r /tmp/db
	-$(RM) -r /tmp/db/is.db
