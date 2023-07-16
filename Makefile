default: build

up:
	./run.sh

stop:
ifdef CONTAINER_NAME
	docker stop $(CONTAINER_NAME)
else
	docker stop gw-discord-ss-bot
endif

restart: stop up

build:
ifdef TAG
	docker build -t $(TAG) .
else
	docker build -t gw-discord-ss-bot .
endif

.PHONY: up down restart build