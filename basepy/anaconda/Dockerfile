FROM continuumio/miniconda
SHELL ["/bin/bash", "-c"]
USER root
WORKDIR /
RUN apt-get -y update \
    && apt-get -y upgrade \
    && apt-get install -y --no-install-recommends gcc build-essential libssl-dev libffi-dev python-dev python3-dev libxml2-dev libxslt1-dev zlib1g-dev g++ libsasl2-dev libldap2-dev libfontconfig1-dev libkrb5-dev libcurl4-openssl-dev
COPY environment.yml /
RUN conda env create -f environment.yml -v
RUN echo "source activate dsms" > ~/.bashrc
ENV PATH /opt/conda/envs/dsms/bin:$PATH