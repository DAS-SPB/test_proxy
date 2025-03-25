from fastapi import FastAPI
from proxy.endpoints import transfer_proxy
from proxy.middleware import LoggingMiddleware

proxy = FastAPI()

proxy.include_router(transfer_proxy.router)
proxy.add_middleware(LoggingMiddleware)


@proxy.get("/health")
def read_root():
    return {"health": "OK"}
