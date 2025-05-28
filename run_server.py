#!/usr/bin/env python3
"""
Command Orchestra Backend Server
Launch script for the FastAPI automation backend.
"""

import os
import sys
import uvicorn
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Launch the FastAPI server."""

    # Check if .env file exists
    env_file = project_root / ".env"
    if not env_file.exists():
        print("⚠️  Warning: .env file not found!")
        print("Please create a .env file with your configuration:")
        print("OBSIDIAN_MAIN_VAULT_PATH=/path/to/your/main/vault")
        print("OBSIDIAN_EXERCISE_VAULT_PATH=/path/to/your/exercise/vault")
        print("OPENAI_API_KEY=your_openai_api_key")
        print()

    print("🎻 Starting Command Orchestra Backend...")
    print("🚀 Server will be available at: http://localhost:8000")
    print("📚 API docs available at: http://localhost:8000/docs")
    print("🔄 Auto-reload enabled for development")
    print()

    try:
        uvicorn.run(
            "speech2action.api.main:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True,
        )
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
