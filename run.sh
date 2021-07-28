#!/usr/bin/env bash

export HOST_UID=$UID
HOST_GID=$(id -g)
export HOST_GID
export PROJECT_DIR=$(realpath .)

help() {
    echo "usage: run.sh [build|start|stop|config|restart]"
}

if [[ "$#" -ge 1 ]]; then
    if [[ "$1" == "start" ]]; then
        docker-compose --project-directory ${PROJECT_DIR} \
        -f ${PROJECT_DIR}/docker-compose.yml \
        up -d
    elif [[ "$1" == "build" ]]; then
        docker-compose --project-directory ${PROJECT_DIR} \
        -f ${PROJECT_DIR}/docker-compose.yml \
        build
    elif [[ "$1" == "stop" ]]; then
        docker-compose --project-directory ${PROJECT_DIR} \
        -f ${PROJECT_DIR}/docker-compose.yml \
        down
    elif [[ "$1" == "config" ]]; then
        docker-compose --project-directory ${PROJECT_DIR} \
        -f ${PROJECT_DIR}/docker-compose.yml \
        config
    elif [[ "$1" == "restart" ]]; then
        docker-compose --project-directory ${PROJECT_DIR} \
        -f ${PROJECT_DIR}/docker-compose.yml \
        restart "$2"
    else
        help
    fi
else
    help
fi
