#!/bin/bash

set -ex

#conf
image_name=weedgummiesbot

# build
docker build -t ${image_name} .

# run with cwd mounted in image
docker run \
    --rm \
    -v `pwd`:/usr/src/app \
    -e BOT_TOKEN \
    ${image_name} ${@}
