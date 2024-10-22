FROM python:3.11
WORKDIR /app
COPY app.py .
RUN pip install --upgrade pip && pip install psycopg[binary] flask
CMD ["flask", "--app", "app", "run", "--host", "0.0.0.0"]
