FROM python:3.12-slim

COPY requirements.txt /temp/requirements.txt
WORKDIR /courses_webinars

RUN apt-get update && apt-get install -y \
  default-libmysqlclient-dev \
  pkg-config \
  ffmpeg \
  gcc \
  python3-dev \
  build-essential \
  && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip setuptools wheel
RUN pip install -r /temp/requirements.txt

COPY courses_webinars /courses_webinars
