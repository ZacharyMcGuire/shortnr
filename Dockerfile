FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_RUN_HOST 0.0.0.0

RUN apk add --no-cache postgresql-dev python3-dev gcc musl-dev linux-headers

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

WORKDIR usr/src/shortnr/
