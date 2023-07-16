#!/usr/bin/env bash

IMAGE_NAME="$1"

if [[ $# -eq 1 ]] ; then
    docker build -t "$IMAGE_NAME" .
else
    docker build -t gw-discord-ss-bot .
fi
