FROM python:3.12.1-slim

WORKDIR /app2

COPY pyproject.toml poetry.lock ./

COPY app2 ./app2

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main

CMD ["uvicorn", "app2.main:app", "--host", "0.0.0.0", "--port", "8000"]
