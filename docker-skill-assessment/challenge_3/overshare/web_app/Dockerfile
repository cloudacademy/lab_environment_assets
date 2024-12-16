# syntax=docker/dockerfile:1
FROM python:3.10-alpine

WORKDIR /code
COPY . .
RUN --mount=type=cache,target=/root/.cache/ python3 -m pip install -r requirements.txt --cache-dir=/root/.cache/ 

ARG ENABLE_FLASK_DEBUG false
ENV FLASK_APP app.py
ENV FLASK_DEBUG $ENABLE_FLASK_DEBUG
ENV FLASK_RUN_PORT 9000
ENV FLASK_RUN_HOST 0.0.0.0
ENV GUNICORN_LOG_LEVEL info

EXPOSE 9000

CMD gunicorn --workers=2 app:app -b "$FLASK_RUN_HOST:$FLASK_RUN_PORT" --log-level="$GUNICORN_LOG_LEVEL"

