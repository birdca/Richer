#!/bin/bash

if [ -x "$(command -v docker)" ]; then
    echo "Already have docker"
else
    echo "Install docker"
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
fi

whoami
docker login -u "richer1018" -p $DOCKER_HUB_TOKEN
docker pull richer1018/crawler:9.0.3
docker stack deploy --with-registry-auth -c crawler.yml financialdata
