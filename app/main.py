import logging
import uuid
import time
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from app.core.logger import setup_logger, request_id_ctx_var

# Configure JSON logging for startup
setup_logger()
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    logger.info("Initializing PageIndex-KnowledgeOS API")
    yield
    # Shutdown logic
    logger.info("Shutting down API")

app = FastAPI(
    title="PageIndex-KnowledgeOS",
    description="Enterprise-grade hierarchical RAG system API",
    version="1.0.0",
    lifespan=lifespan
)

@app.middleware("http")
async def log_request_middleware(request: Request, call_next):
    # Assign a unique ID to every request
    request_id = str(uuid.uuid4())
    request_id_ctx_var.set(request_id)
    
    start_time = time.time()
    logger.info(f"Request started: {request.method} {request.url.path}")
    
    try:
        response = await call_next(request)
        process_time = time.time() - start_time
        logger.info(
            f"Request completed: {request.method} {request.url.path}",
            extra={"latency_s": round(process_time, 4), "status_code": response.status_code}
        )
        return response
    except Exception as e:
        process_time = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url.path}",
            extra={"latency_s": round(process_time, 4), "error": str(e)},
            exc_info=True
        )
        raise

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}
