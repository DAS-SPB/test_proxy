from fastapi import FastAPI
from proxy.endpoints import transfer_proxy

proxy = FastAPI()

proxy.include_router(transfer_proxy.router)


@proxy.get("/health")
def read_root():
    return {"health": "OK"}
