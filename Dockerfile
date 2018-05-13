###
# Replace:
# ${docker_username} -> docker_username
# ${docker_project} -> docker_project
# from basepy Dockerfile
###
FROM ${docker_username}/basepy_${docker_project}:latest

USER root
WORKDIR /
RUN mkdir dsms && mkdir dsms/data && mkdir dsms/src
COPY src dsms/src/
COPY run.sh /dsms/

WORKDIR /dsms/
ENV PORT 9000
EXPOSE $PORT
CMD ./run.sh