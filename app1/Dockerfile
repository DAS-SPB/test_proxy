FROM python:3.12.1-slim

WORKDIR /app1

COPY pyproject.toml poetry.lock ./

COPY app1 ./app1

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main

CMD ["uvicorn", "app1.main:app", "--host", "0.0.0.0", "--port", "8000"]
