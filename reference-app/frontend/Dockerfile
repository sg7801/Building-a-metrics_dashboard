# Use the official Python image.
# https://hub.docker.com/_/python
FROM python:3.7-slim

ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV PROMETHEUS_MULTIPROC_DIR /app
ENV prometheus_multiproc_dir /app

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-w", "4", "-b", "0.0.0.0:8080", "app:app"]
