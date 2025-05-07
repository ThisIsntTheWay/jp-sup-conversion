#!/bin/env python3
# vobsub2png fails to install on versions around 1.86
FROM rust:1.82 AS vobsub
RUN cargo install vobsub2png@0.1.4

# -------------------------------
FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y openjdk-17-jre && \
    apt-get clean

COPY --from=vobsub /usr/local/cargo/bin/vobsub2png /bin/vobsub2png

WORKDIR /app
ADD https://raw.githubusercontent.com/wiki/mjuhasz/BDSup2Sub/downloads/BDSup2Sub.jar /app/BDSup2Sub.jar

COPY main.py /app
COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt
ENTRYPOINT [ "python3", "/app/main.py" ]
