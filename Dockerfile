ARG BASE_IMAGE=myorg/myapp:latest
FROM $BASE_IMAGE

USER root
WORKDIR /
RUN mkdir dsms && mkdir dsms/data && mkdir dsms/src
COPY src dsms/src/
COPY run.sh /dsms/

WORKDIR /dsms/
ENV PORT 9000
EXPOSE $PORT
CMD ./run.sh