#!/bin/bash

set -x

#conf
: ${image_name:=weedgummiesbot}
: ${env_file:=example.env}

container_name=${image_name}:export
container_label=export

# build
docker build -t ${container_name} . || exit 1

# run with cwd mounted in image
docker run \
    --env-file ${env_file} \
    --entrypoint python \
    --label ${container_label} \
    ${container_name} -u export.py

# cleanup docker
docker rm `docker ps -a -f label=${container_label} -q | tail -n +2` || true