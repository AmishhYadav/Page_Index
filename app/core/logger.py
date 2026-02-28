import logging
from pythonjsonlogger import jsonlogger
import contextvars
import uuid

# Context variable for request IDs
request_id_ctx_var: contextvars.ContextVar[str] = contextvars.ContextVar(
    "request_id", default=""
)

class RequestIdFilter(logging.Filter):
    def filter(self, record):
        request_id = request_id_ctx_var.get()
        if request_id:
            record.request_id = request_id
        return True

def setup_logger():
    # Only configure if not already configured by root
    logger = logging.getLogger()
    
    # Remove all existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        
    logHandler = logging.StreamHandler()
    formatter = jsonlogger.JsonFormatter(
        '%(timestamp)s %(level)s %(name)s %(message)s',
        rename_fields={"levelname": "level", "asctime": "timestamp"}
    )
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)
    logger.setLevel(logging.INFO)
    logger.addFilter(RequestIdFilter())
