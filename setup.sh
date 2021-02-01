#!/usr/bin/env bash

project_name="dsms"
docker_username="anktksh"
project_version=1.0.0
anaconda=true # false will use python 3
push_images=false

basedir=`pwd`

# Setting basepy image
if [ ${anaconda} = true ]; then
    echo "Building base python docker image from Anaconda python"
    cd basepy/anaconda && docker build -t ${docker_username}/basepy_${project_name}:${project_version} . && cd ${basedir}
else
    echo "Building base python docker image from vanilla python"
    cd basepy/py && docker build -t ${docker_username}/basepy_${project_name}:${project_version} . && cd ${basedir}
fi

# Setting main docker image
cd ${basedir}
echo "Building main docker image"
docker build -t ${docker_username}/${project_name}:${project_version} --build-arg BASE_IMAGE=${docker_username}/basepy_${project_name}:${project_version} .

if [ ${push_images} = true ]; then
    echo "Pushing docker images to repository"
    docker push ${docker_username}/basepy_${project_name}:${project_version}
    docker push ${docker_username}/${project_name}:${project_version}
fi
