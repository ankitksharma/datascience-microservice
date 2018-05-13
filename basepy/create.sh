#!/usr/bin/env bash
export docker_username='yourdockerusername'
export docker_project='dsms'

docker build -t ${docker_username}/basepy_${docker_project}:latest .
docker push ${docker_username}/basepy_${docker_project}:latest