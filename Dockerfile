# pull official base image
FROM python:3.8.1-alpine

# set working directory
# RUN mkdir -p /usr/src/app
WORKDIR = /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents buffering io
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD flask run -h 0.0.0.0