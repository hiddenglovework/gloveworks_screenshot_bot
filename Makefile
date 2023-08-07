default: build

up:
ifdef BUILD
	./run.sh -c .config -b
else
	./run.sh -c .config
endif

stop:
ifdef CONTAINER_NAME
	docker stop $(CONTAINER_NAME)
else
	docker stop gw-discord-ss-bot
endif

restart: stop up

.PHONY: up down restart