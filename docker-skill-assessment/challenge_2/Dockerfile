FROM python:3.11
WORKDIR /runtime
COPY app.py .
RUN pip install --upgrade pip && pip install "psycopg[binary]"
CMD ["python3", "app.py"]
