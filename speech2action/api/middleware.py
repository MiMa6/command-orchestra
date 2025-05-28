"""Middleware for FastAPI application."""

import time
import logging
from fastapi import Request, Response
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware

logger = logging.getLogger(__name__)


class LoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log API requests and responses."""

    async def dispatch(self, request: Request, call_next):
        start_time = time.time()

        # Log request
        logger.info(f"Request: {request.method} {request.url}")

        # Process request
        response = await call_next(request)

        # Calculate processing time
        process_time = time.time() - start_time

        # Log response
        logger.info(
            f"Response: {response.status_code} | "
            f"Processing time: {process_time:.4f}s"
        )

        # Add processing time header
        response.headers["X-Process-Time"] = str(process_time)

        return response


def setup_cors_middleware(app):
    """Setup CORS middleware for the FastAPI app."""

    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",  # React development server
            "http://localhost:5173",  # Vite development server
            "http://localhost:8083",  # Custom frontend port
            "http://127.0.0.1:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:8083",
            # Add your production frontend URL here
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Add logging middleware
    app.add_middleware(LoggingMiddleware)
