FROM python:3.11-slim

COPY requirements.txt /temp/requirements.txt
WORKDIR /courses_webinars

RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  pkg-config \
  ffmpeg \
  gcc \
  && rm -rf /var/lib/apt/lists/*

RUN pip install -r /temp/requirements.txt

COPY courses_webinars /courses_webinars
