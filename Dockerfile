FROM python:2.7.14
MAINTAINER Robert (rob@robcovington.com)

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update && \
	pip install lxml ncclient

ADD tempmon.py /
RUN chmod a+x tempmon.py
 
VOLUME /data
