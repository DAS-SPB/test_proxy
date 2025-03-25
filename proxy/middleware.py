import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request

logger = logging.getLogger("proxy_logger")
logger.setLevel(logging.INFO)

handler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        request_body = await request.body()
        logger.info(
            f"Incoming request at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}: "
            f"method={request.method}, url={request.url}, headers={dict(request.headers)}, "
            f"body={request_body.decode('utf-8') if request_body else None}"
        )

        response = await call_next(request)
        process_time = time.time() - start_time

        try:
            response_body = response.body.decode('utf-8') if response.body else None
        except Exception as e:
            response_body = "Could not decode response body"

        logger.info(
            f"Outgoing response at {time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())}: "
            f"status_code={response.status_code}, headers={dict(response.headers)}, "
            f"body={response_body}, process_time={process_time:.2f}s"
        )
        return response
