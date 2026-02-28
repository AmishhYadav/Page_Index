import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI

# Configure basic logging for startup
logging.basicConfig(level=logging.INFO)
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

@app.get("/api/v1/health")
async def health_check():
    return {"status": "ok"}
