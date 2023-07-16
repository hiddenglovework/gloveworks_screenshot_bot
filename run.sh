#!/usr/bin/env bash

TOKEN=""
ID=""
IMAGE="gw-discord-ss-bot"
CONTAINER_NAME="gw-discord-ss-bot"

usage() {
    echo "Usage: ./run.sh -t <discord-token> [-id <channel-id>] [-img <docker-image>] [-c <config-file>]"
    echo "Options:"
    echo "  -t, --token <discord-token>   Specify the Discord token.             (Required if config flags is not passed)"
    echo "  -id, --id <id>                Specify the Discord channel ID.        (Optional)"
    echo "  -img, --image <id>            Specify the Docker image.              (Optional)"
    echo "  -c, --config <config-file>    Specify the configuration file.        (Required if token flags is not passed)"
    echo "                                                                       NOTE: The config file needs to have an empty line at the end"
    echo
}

parse_config() {
    local config_file="$1"
    while IFS='=' read -r key value; do
        key=$(echo "$key" | tr -d '[:space:]' | tr '[:upper:]' '[:lower:]')
        value=$(echo "$value" | sed 's/^ *//; s/ *$//; s/"//g')
        case $key in
            token)
                TOKEN="$value"
                ;;
            id)
                ID="$value"
                ;;
            image)
                IMAGE="$value"
                ;;
            container_name)
                CONTAINER_NAME="$value"
                ;;
            *)
                echo "Invalid key: $key" >&2
                exit 1
                ;;
        esac
    done < "$config_file"
}

parse_flags() {
    while [[ $# -gt 0 ]]; do
        key="$1"
        case $key in
            -t|--token)
                TOKEN="$2"
                shift
                shift
                ;;
            -id|--id)
                ID="$2"
                shift
                shift
                ;;
            -img|--image)
                IMAGE="$2"
                shift
                shift
                ;;
            -c|--config)
                parse_config "$2"
                shift
                shift
                ;;
            -h|--help)
                usage
                exit 0
                ;;
            *)
                echo "Invalid option: $key" >&2
                usage
                exit 1
                ;;
        esac
    done
}

if [[ $# -eq 0 ]]; then
    echo "Script requires arguments."
    echo
    usage
    exit 1
fi

parse_flags "$@"

if [[ -z "$TOKEN" ]]; then
    echo "Token is required."
    echo
    usage
    exit 1
fi

echo "$TOKEN $ID $IMAGE $CONTAINER_NAME"

docker run -d --rm \
    -p 4444:4444 \
    -p 5900 \
    -p 7900:7900 \
    -v $PWD:$PWD -w $PWD --shm-size 2g \
    -e DISCORD_TOKEN="$TOKEN" -e CHANNEL_ID="$ID" \
    "$IMAGE" "$CONTAINER_NAME"


sleep 5