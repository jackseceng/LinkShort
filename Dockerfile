FROM python:3.7.3-alpine3.9 as base

#Dev docker image
RUN mkdir /work/
WORKDIR /work/

COPY ./src/requirements.txt /work/requirements.txt
RUN pip3 install --no-cache-dir --upgrade pip && pip3 install -r requirements.txt