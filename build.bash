#!/bin/bash
if [[ $# -eq 1 ]] ; then
    docker build -t $1 .
else
    docker build .
fi
