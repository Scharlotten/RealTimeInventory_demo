FROM python:3.7-slim

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install -U -r /tmp/requirements.txt

ENV PYTHONUNBUFFERED 1

COPY *.py ./

ENTRYPOINT python3.7 ./change_customers.py
