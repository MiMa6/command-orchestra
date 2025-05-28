"""FastAPI application for Command Orchestra automation backend."""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles

from .routes import router
from .middleware import setup_cors_middleware

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    logger.info("🎻 Command Orchestra backend starting up...")
    yield
    logger.info("🎻 Command Orchestra backend shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Command Orchestra API",
    description="Speech-2-Reality Automation Hub Backend",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Setup middleware
setup_cors_middleware(app)

# Include routes
app.include_router(router, prefix="/api/v1", tags=["automations"])


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint with API information."""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Command Orchestra API</title>
        <style>
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 2rem;
                background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
                color: white;
                min-height: 100vh;
            }
            .header {
                text-align: center;
                margin-bottom: 2rem;
            }
            .title {
                font-size: 3rem;
                margin: 0;
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            .subtitle {
                font-size: 1.2rem;
                opacity: 0.8;
                margin: 0.5rem 0;
            }
            .endpoints {
                background: rgba(255, 255, 255, 0.1);
                border-radius: 12px;
                padding: 1.5rem;
                margin: 1rem 0;
            }
            .endpoint {
                margin: 1rem 0;
                padding: 1rem;
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                border-left: 4px solid #4ecdc4;
            }
            .method {
                display: inline-block;
                background: #4ecdc4;
                color: #1a1a2e;
                padding: 0.25rem 0.5rem;
                border-radius: 4px;
                font-weight: bold;
                font-size: 0.8rem;
            }
            .path {
                font-family: 'Monaco', 'Consolas', monospace;
                font-weight: bold;
                margin-left: 0.5rem;
            }
            .description {
                margin-top: 0.5rem;
                opacity: 0.9;
            }
            a {
                color: #4ecdc4;
                text-decoration: none;
            }
            a:hover {
                text-decoration: underline;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1 class="title">🎻 Command Orchestra🪄</h1>
            <p class="subtitle">"Orchestrate life with your voice 🗣️✨"</p>
            <p>Speech-2-Reality Automation Hub</p>
        </div>
        
        <div class="endpoints">
            <h2>🚀 API Endpoints</h2>
            
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="path">/api/v1/workout</span>
                <div class="description">Trigger workout-related Obsidian automations (running, cycling, mobility, gym)</div>
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="path">/api/v1/studio</span>
                <div class="description">Launch FL Studio and configure audio settings</div>
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="path">/api/v1/daily-note</span>
                <div class="description">Create daily notes in Obsidian vault</div>
            </div>
            
            <div class="endpoint">
                <span class="method">POST</span>
                <span class="path">/api/v1/voice-command</span>
                <div class="description">Process natural language voice commands</div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span>
                <span class="path">/api/v1/automations</span>
                <div class="description">List all available automation endpoints</div>
            </div>
            
            <div class="endpoint">
                <span class="method">GET</span>
                <span class="path">/api/v1/health</span>
                <div class="description">Health check endpoint</div>
            </div>
        </div>
        
        <div class="endpoints">
            <h2>📚 Documentation</h2>
            <p>
                • <a href="/docs">Interactive API Documentation (Swagger UI)</a><br>
                • <a href="/redoc">Alternative API Documentation (ReDoc)</a><br>
                • <a href="/api/v1/automations">Available Automations List</a>
            </p>
        </div>
        
        <div class="endpoints">
            <h2>🛠️ Development</h2>
            <p>
                Server is running in development mode.<br>
                Make sure your frontend is configured to connect to this backend.
            </p>
        </div>
    </body>
    </html>
    """


@app.get("/api/v1")
async def api_info():
    """API information endpoint."""
    return {
        "name": "Command Orchestra API",
        "version": "1.0.0",
        "description": "Speech-2-Reality Automation Hub Backend",
        "docs_url": "/docs",
        "automations_url": "/api/v1/automations",
        "health_url": "/api/v1/health",
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "speech2action.api.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
