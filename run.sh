#!/bin/bash

set -ex

#conf
: ${image_name=weedgummiesbot}
: ${env_file=.env/prod.env}

# build
docker build -t ${image_name} .

# run with cwd mounted in image
docker run \
    --rm \
    -v `pwd`:/usr/src/app \
    --env-file ${env_file} \
    ${image_name} ${@}
