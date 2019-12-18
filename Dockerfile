FROM python:3.8 AS base

WORKDIR /app
COPY main/requirements.txt /app
RUN apt-get update && apt-get install --no-install-recommends -y gcc build-essential unixodbc-dev && apt-get clean && rm -rf /var/lib/apt/lists/*
RUN pip install --user -r requirements.txt
COPY main/*.py /app

CMD ["python", "main.py"]