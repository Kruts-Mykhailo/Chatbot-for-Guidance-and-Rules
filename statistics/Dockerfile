FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    g++ \
    libffi-dev \
    libssl-dev \
    make \
    libblas-dev \
    liblapack-dev \
    libatlas-base-dev \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY statistics/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY statistics/app /app
COPY statistics/data /data

EXPOSE 9090

CMD ["python", "-m", "app.main"]