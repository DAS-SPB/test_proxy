FROM python:3.12.1-slim

WORKDIR /proxy

COPY pyproject.toml poetry.lock ./

COPY proxy ./proxy

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only main --no-root

CMD ["python", "-m", "uvicorn", "proxy.main:app", "--host", "0.0.0.0", "--port", "8003"]
