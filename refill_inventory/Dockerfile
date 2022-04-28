FROM python:3.7-slim

COPY requirements.txt /tmp/requirements.txt
COPY producer.config /tmp/producer.config
RUN pip3 install -U -r /tmp/requirements.txt

ENV PYTHONUNBUFFERED 1

WORKDIR /refill_inventory