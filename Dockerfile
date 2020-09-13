FROM python:3.8-buster

COPY scrapnow/ /opt/scrapnow/

WORKDIR /opt/scrapnow/
RUN python setup.py sdist && pip install dist/*
