#!/bin/bash

TOKEN=""

if [[ -z $TOKEN ]] ; then
    printf "Please edit this script and input an Discord API Token"
    exit 1
elif [[ $# -eq 1 ]] ; then
    docker run -d --rm -p 4444:4444 -p 5900:5900 \
    -p 7900:7900 -v $PWD:$PWD -w $PWD --shm-size 2g \
    -e DISCORD_TOKEN=${TOKEN} $1 gw-discord-ss-bot
else
    docker run -d --rm -p 4444:4444 -p 5900:5900 \
    -p 7900:7900 -v $PWD:$PWD -w $PWD --shm-size 2g \
    -e DISCORD_TOKEN=${TOKEN} hiddenglovework/ss-discordbot:v1.0.0 gw-discord-ss-bot
fi
