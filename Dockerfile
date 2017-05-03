FROM ubuntu:16.04

RUN apt-get update -y
RUN apt-get install -y git python3-pip curl
RUN python3 -m pip install --upgrade pip pytest-cov nbval \
      git+git://github.com/joommf/joommfutil.git \
      git+git://github.com/joommf/discretisedfield.git

WORKDIR /usr/local
RUN git clone https://github.com/joommf/micromagneticmodel.git

WORKDIR /usr/local/micromagneticmodel