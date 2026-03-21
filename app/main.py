"""
FastAPI Main Application
"""
import os
import time
import json
import asyncio
import httpx
from fastapi import FastAPI, Request
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

@app.middleware("http")
async def log_requests_and_responses(request: Request, call_next):
    """Middleware to log all requests and responses for debugging on Render"""
    # Skip logging for health endpoints to avoid log spam
    skip_paths = ["/health", "/", "/health/", f"{settings.API_V1_STR}/health", f"{settings.API_V1_STR}/health/"]
    if request.url.path in skip_paths:
        return await call_next(request)
        
    start_time = time.time()
    
    # Extract request body
    req_body_str = None
    try:
        body_bytes = await request.body()
        if body_bytes:
            req_body_str = body_bytes.decode("utf-8")
            # Try to parse as JSON for cleaner logging if possible
            try:
                # We just verify it's JSON, but log as string or parsed object
                json.loads(req_body_str)
            except json.JSONDecodeError:
                pass
                
        # Reset the request body so endpoints can read it
        async def receive():
            return {"type": "http.request", "body": body_bytes}
        request._receive = receive
    except Exception as e:
        logger.error(f"Error reading request body: {str(e)}")

    req_details = {
        "method": request.method,
        "path": request.url.path,
        "query": request.url.query,
    }
    if req_body_str:
        req_details["body"] = req_body_str

    # Log incoming request
    logger.info(f"API Request: {request.method} {request.url.path}", extra={"extra": {"request": req_details}})

    # Process the request
    response = await call_next(request)
    
    # Calculate process time
    process_time = (time.time() - start_time) * 1000
    
    # Extract response body
    res_body_str = None
    try:
        if hasattr(response, "body_iterator"):
            res_body_bytes = b""
            async for chunk in response.body_iterator:
                res_body_bytes += chunk
            
            # Reset the body iterator so the client gets the response
            async def new_body_iterator():
                yield res_body_bytes
            response.body_iterator = new_body_iterator()
            
            res_body_str = res_body_bytes.decode("utf-8")
            # Truncate very long responses
            if len(res_body_str) > 2000:
                res_body_str = res_body_str[:2000] + "... [truncated]"
    except Exception as e:
        logger.error(f"Error reading response body: {str(e)}")
        
    res_details = {
        "status_code": response.status_code,
        "process_time_ms": round(process_time, 2)
    }
    if res_body_str:
        res_details["body"] = res_body_str
        
    # Log outgoing response
    logger.info(
        f"API Response: {request.method} {request.url.path} - Status: {response.status_code}", 
        extra={"extra": {"response": res_details}}
    )
    
    return response

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

