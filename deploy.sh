#!/bin/bash

set -ex

#conf
: ${git_branch:=`git rev-parse --abbrev-ref HEAD`}
: ${image_name:=weedgummiesbot}
: ${env_file:=.env/prod.env}
git_hash=`git rev-parse HEAD`

# build
container_version=${image_name}:${git_branch}-${git_hash:0:5}
docker build -t ${container_version} .

# stop old container
running_container=`docker ps --filter="name=${image_name}_${git_branch}" -q`
if [ -n "${running_container}" ]; then
    docker stop ${running_container}
    docker rm ${running_container}
fi

# start new container in headless/always on mode
docker run \
    -d \
    --restart always \
    --env-file ${env_file} \
    --env VERSION=${container_version} \
    --env SCHEDULE_ENABLED=False \
    --name ${image_name}_${git_branch} \
    ${container_version}
