import logging
import time

from flask import g, request


def register_request_logging(app):
    logging.basicConfig(level=getattr(logging, app.config.get("LOG_LEVEL", "INFO")))

    @app.before_request
    def start_timer():
        g.request_started_at = time.perf_counter()

    @app.after_request
    def log_request(response):
        elapsed_ms = (time.perf_counter() - g.get("request_started_at", time.perf_counter())) * 1000
        app.logger.info(
            "%s %s -> %s %.2fms",
            request.method,
            request.path,
            response.status_code,
            elapsed_ms,
        )
        return response
