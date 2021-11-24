FROM python:3.7-sli
ENV APP_HOME /app
WORKDIR $APP_HOME
COPY . ./

ENV PROMETHEUS_MULTIPROC_DIR /app
ENV prometheus_multiproc_dir /app

RUN apt-get update && \
    pip install --upgrade pip && \
    pip install -r requirements.txt

EXPOSE 8082

CMD ["gunicorn", "--access-logfile", "-", "--error-logfile", "-", "-c", "config.py", "-w", "4", "-b", "0.0.0.0:8082", "app:app"]
