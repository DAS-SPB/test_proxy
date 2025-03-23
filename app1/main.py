from fastapi import FastAPI
from app1.endpoints import auth, payment

PREFIX = "/app1"

app1 = FastAPI()

app1.include_router(auth.router, prefix=PREFIX)
app1.include_router(payment.router, prefix=PREFIX)


@app1.get("/health")
def read_root():
    return {"health": "OK"}
