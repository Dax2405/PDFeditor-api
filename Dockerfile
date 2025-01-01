FROM python:3.13-slim

WORKDIR /app

COPY requirements.txt requirements.txt
COPY main.py main.py
COPY README.md README.md

RUN apt-get update && apt-get install -y \
    ghostscript \
    clamav \
    && rm -rf /var/lib/apt/lists/*

RUN freshclam


RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8001

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]