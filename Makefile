#!/usr/bin/make -f
# -*- mode:makefile -*-

NODES=$(basename $(shell ls node*.config | sort -r))
NODE_DIRS=$(addprefix /tmp/db/, $(NODES))
IG_ADMIN=icegridadmin --Ice.Config=locator.config -u user -p pass

start-grid: /tmp/db/registry $(NODE_DIRS)
	icegridnode --Ice.Config=node1.config &
	@echo -- ok

stop-grid:
	@for node in $(NODES); do \
	    $(IG_ADMIN) -e "node shutdown $$node"; \
	done

	@killall icegridnode
	@echo -- ok

show-nodes:
	$(IG_ADMIN) -e "node list"

/tmp/db/%:
	mkdir -p $@

clean: stop-grid
	-$(RM) *~
	-$(RM) -r /tmp/db
