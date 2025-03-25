from fastapi import FastAPI
from app2.endpoints import transfer

PREFIX = "/app2"

app2 = FastAPI()

app2.include_router(transfer.router, prefix=PREFIX)


@app2.get("/health")
def read_root():
    return {"health": "OK"}
