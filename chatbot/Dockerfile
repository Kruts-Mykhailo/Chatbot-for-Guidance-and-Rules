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

COPY chatbot/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

EXPOSE 8080

CMD ["python", "-m", "app.main", "--search_type=pgvector", "--generator_type=sentence_transformer", "--model_type=openai", "--secret_type=local"]