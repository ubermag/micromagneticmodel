FROM ubuntu:18.04

RUN apt-get update -y
RUN apt-get install -y git python3-pip curl
RUN python3 -m pip install --upgrade pip pytest-cov nbval \
      git+git://github.com/joommf/joommfutil.git \
      git+git://github.com/joommf/discretisedfield.git

COPY . /usr/local/micromagneticmodel/
WORKDIR /usr/local/micromagneticmodel
RUN python3 -m pip install .
