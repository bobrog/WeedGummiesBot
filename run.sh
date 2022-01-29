#!/bin/bash

set -ex

#conf
: ${git_branch:=`git rev-parse --abbrev-ref HEAD`}
: ${image_name:=weedgummiesbot}
: ${env_file:=example.env}

# build
docker build -t ${image_name} .

# run with cwd mounted in image
docker run \
    --rm \
    -v `pwd`:/usr/src/app \
    --env-file ${env_file} \
    --env VERSION="${image_name}:${git_branch}" \
    ${image_name} ${@}
