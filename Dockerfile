FROM python:3.8-alpine

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV FLASK_APP shortnr
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_ENV=development
ENV SECRET_KEY=change_me

RUN apk add --no-cache gcc musl-dev linux-headers

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY shortnr/ usr/src/shortnr/
