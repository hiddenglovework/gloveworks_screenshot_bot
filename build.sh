#!/usr/bin/env bash

IMAGE_TAG="$1"

if [[ $# -eq 1 ]] ; then
    docker build -t "$IMAGE_TAG" .
else
    docker build .
fi
