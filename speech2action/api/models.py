"""Pydantic models for API request and response schemas."""

from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime


class AutomationResponse(BaseModel):
    """Standard response model for automation triggers."""

    success: bool
    message: str
    timestamp: datetime
    automation_type: str


class WorkoutRequest(BaseModel):
    """Request model for workout-related automations."""

    workout_type: Literal["running", "cycling", "mobility", "gym"]
    date: Optional[str] = None  # YYYY-MM-DD format, defaults to today


class DailyNoteRequest(BaseModel):
    """Request model for daily note creation."""

    date: Optional[str] = None  # YYYY-MM-DD format, defaults to today
    note_type: Literal["today", "tomorrow"] = "today"


class StudioModeRequest(BaseModel):
    """Request model for FL Studio automation."""

    action: Literal["open_session", "switch_audio", "open_project"] = "open_session"


class VoiceCommandRequest(BaseModel):
    """Request model for voice command processing."""

    command: str
    use_agent: bool = False


class HealthCheckResponse(BaseModel):
    """Health check response model."""

    status: str
    version: str
    timestamp: datetime
