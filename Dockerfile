# syntax=docker/dockerfile:1
FROM python:3
WORKDIR /chatroom
COPY requirements.txt /chatroom/
RUN pip install -r requirements.txt
COPY . /chatroom/