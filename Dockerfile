# pull official base image
FROM python:3.8.1-alpine

RUN apk update && \
    apk add --virtual build-deps gcc python-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents buffering io
ENV PYTHONUNBUFFERED 1
ENV APP_SETTINGS=project.config.DevelopmentConfig
ENV FLASK_ENV=development

# set working directory
# RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

# add and install requirements
# Do this first because I'm installing the app as a package
COPY . /usr/src/app
# COPY ./requirements.txt /usr/src/app/requirements.txt
# COPY ./requirements_dev.txt /usr/src/app/requirements_dev.txt
RUN pip install --upgrade pip
RUN pip install -r requirements_dev.txt

COPY ./entrypoint.sh /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

