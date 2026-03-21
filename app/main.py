"""
FastAPI Main Application
"""
import os
import asyncio
import httpx
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.core.config import settings
from app.api.v1.api import api_router
from app.core.exceptions import setup_exception_handlers
from app.core.firebase import initialize_firebase
from app.core.logging import logger


async def keep_alive_task():
    """Background task to fetch the health endpoint every 14 minutes to prevent Render from sleeping."""
    url = os.environ.get("RENDER_EXTERNAL_URL", "")
    if not url:
        logger.warning("RENDER_EXTERNAL_URL not set. Falling back to localhost:10000 for keep-alive.")
        url = "http://127.0.0.1:10000"
    
    health_url = f"{url.rstrip('/')}/health"
    logger.info(f"Starting keep-alive background task polling {health_url} every 14 minutes")
    
    async with httpx.AsyncClient() as client:
        while True:
            await asyncio.sleep(14 * 60)  # Sleep for 14 minutes
            try:
                response = await client.get(health_url, timeout=10.0)
                logger.info(f"[Keep-Alive] Ping {health_url} - Status: {response.status_code}")
            except Exception as e:
                logger.error(f"[Keep-Alive] Ping failed: {str(e)}")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting Londa API...")
    try:
        initialize_firebase()
        logger.info("Firebase initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {str(e)}")
        # Continue anyway for development
        
    try:
        import cloudinary
        if settings.CLOUDINARY_URL:
            cloudinary.config(url=settings.CLOUDINARY_URL)
            logger.info("Cloudinary initialized successfully")
    except Exception as e:
        logger.error(f"Failed to initialize Cloudinary: {str(e)}")
    
    # Start keep alive task
    keep_alive = asyncio.create_task(keep_alive_task())
    
    yield
    
    # Shutdown
    logger.info("Shutting down Londa API...")
    keep_alive.cancel()
    try:
        await keep_alive
    except asyncio.CancelledError:
        pass


# Create FastAPI application instance
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Setup CORS middleware
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# Setup exception handlers
setup_exception_handlers(app)

# Include API router
app.include_router(api_router, prefix=settings.API_V1_STR)


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": f"Welcome to {settings.PROJECT_NAME}",
        "version": settings.VERSION,
        "docs": "/docs",
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from app.core.responses import success_response
    return success_response(
        message="Service is healthy",
        data={
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION
        }
    )


@app.get("/test")
async def test():
    """Test endpoint to verify API Gateway JSON responses"""
    from app.core.responses import success_response
    return success_response(
        message="API Gateway is working correctly",
        data={
            "status": "ok",
            "service": settings.PROJECT_NAME
        }
    )

