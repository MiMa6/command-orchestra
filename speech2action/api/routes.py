"""FastAPI routes for automation triggers."""

import logging
from datetime import datetime
from typing import Dict, Any

from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse

from .models import (
    AutomationResponse,
    WorkoutRequest,
    DailyNoteRequest,
    StudioModeRequest,
    VoiceCommandRequest,
    HealthCheckResponse,
)

# Import automation functions
from speech2action.actions.obsidian_automation import (
    create_gym_dir,
    create_today_running_note,
    create_today_cycling_note,
    create_today_mobility_note,
    create_daily_note,
    create_tomorrow_note,
)
from speech2action.actions.flstudio_automation import (
    open_drum_session,
    launch_fl_studio,
    switch_audio_device,
)
from speech2action.core.command_parser import parse_command
from speech2action.core.action_dispatcher import dispatch_action

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create router
router = APIRouter()


def create_automation_response(
    success: bool, message: str, automation_type: str
) -> AutomationResponse:
    """Helper function to create standardized automation responses."""
    return AutomationResponse(
        success=success,
        message=message,
        timestamp=datetime.now(),
        automation_type=automation_type,
    )


async def run_automation_safely(automation_func, automation_type: str, **kwargs):
    """Safely execute automation function and return standardized response."""
    try:
        logger.info(f"Executing {automation_type} automation")

        # Execute the automation function
        if kwargs:
            result = automation_func(**kwargs)
        else:
            result = automation_func()

        return create_automation_response(
            success=True,
            message=f"{automation_type} automation completed successfully",
            automation_type=automation_type,
        )
    except Exception as e:
        logger.error(f"Error in {automation_type} automation: {str(e)}")
        return create_automation_response(
            success=False,
            message=f"Failed to execute {automation_type} automation: {str(e)}",
            automation_type=automation_type,
        )


@router.get("/health", response_model=HealthCheckResponse)
async def health_check():
    """Health check endpoint."""
    return HealthCheckResponse(
        status="healthy", version="1.0.0", timestamp=datetime.now()
    )


@router.post("/workout", response_model=AutomationResponse)
async def trigger_workout_automation(
    request: WorkoutRequest, background_tasks: BackgroundTasks
):
    """Trigger workout-related Obsidian automations."""

    workout_type = request.workout_type.lower()

    # Map workout types to automation functions
    workout_functions = {
        "running": create_today_running_note,
        "cycling": create_today_cycling_note,
        "mobility": create_today_mobility_note,
        "gym": create_gym_dir,
    }

    if workout_type not in workout_functions:
        raise HTTPException(
            status_code=400, detail=f"Invalid workout type: {workout_type}"
        )

    automation_func = workout_functions[workout_type]

    # Execute automation in background for better responsiveness
    background_tasks.add_task(automation_func)

    return create_automation_response(
        success=True,
        message=f"{workout_type.title()} automation triggered successfully",
        automation_type=f"workout_{workout_type}",
    )


@router.post("/daily-note", response_model=AutomationResponse)
async def trigger_daily_note_automation(
    request: DailyNoteRequest, background_tasks: BackgroundTasks
):
    """Trigger daily note creation in Obsidian."""

    note_type = request.note_type.lower()

    # Map note types to automation functions
    note_functions = {
        "today": create_daily_note,
        "tomorrow": create_tomorrow_note,
    }

    if note_type not in note_functions:
        raise HTTPException(status_code=400, detail=f"Invalid note type: {note_type}")

    automation_func = note_functions[note_type]

    # Execute automation in background
    background_tasks.add_task(automation_func)

    return create_automation_response(
        success=True,
        message=f"{note_type.title()} note automation triggered successfully",
        automation_type=f"daily_note_{note_type}",
    )


@router.post("/studio", response_model=AutomationResponse)
async def trigger_studio_automation(
    request: StudioModeRequest, background_tasks: BackgroundTasks
):
    """Trigger FL Studio automation."""

    action = request.action.lower()

    # Map actions to automation functions
    studio_functions = {
        "open_session": open_drum_session,
        "switch_audio": switch_audio_device,
        "open_project": launch_fl_studio,
    }

    if action not in studio_functions:
        raise HTTPException(status_code=400, detail=f"Invalid studio action: {action}")

    automation_func = studio_functions[action]

    # Execute automation in background
    background_tasks.add_task(automation_func)

    return create_automation_response(
        success=True,
        message=f"FL Studio {action.replace('_', ' ')} automation triggered successfully",
        automation_type=f"studio_{action}",
    )


@router.post("/voice-command", response_model=AutomationResponse)
async def process_voice_command(
    request: VoiceCommandRequest, background_tasks: BackgroundTasks
):
    """Process voice commands through the existing speech2action system."""

    try:
        if request.use_agent:
            # For agent mode, pass the raw command text directly
            background_tasks.add_task(dispatch_action, request.command, use_agent=True)
        else:
            # For traditional mode, parse the command first
            parsed_command = parse_command(request.command)

            if not parsed_command:
                raise HTTPException(
                    status_code=400, detail="Could not parse the voice command"
                )

            # Dispatch action using existing dispatcher
            background_tasks.add_task(dispatch_action, parsed_command, use_agent=False)

        return create_automation_response(
            success=True,
            message=f"Voice command '{request.command}' processed successfully",
            automation_type="voice_command",
        )

    except Exception as e:
        logger.error(f"Error processing voice command: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"Failed to process voice command: {str(e)}"
        )


@router.get("/automations")
async def list_available_automations():
    """List all available automation endpoints and their descriptions."""

    automations = {
        "workout_automations": {
            "endpoint": "/workout",
            "method": "POST",
            "description": "Trigger workout-related Obsidian note automations",
            "supported_types": ["running", "cycling", "mobility", "gym"],
            "example": {"workout_type": "running", "date": "2024-01-15"},  # Optional
        },
        "daily_note_automations": {
            "endpoint": "/daily-note",
            "method": "POST",
            "description": "Create daily notes in Obsidian vault",
            "supported_types": ["today", "tomorrow"],
            "example": {"note_type": "today", "date": "2024-01-15"},  # Optional
        },
        "studio_automations": {
            "endpoint": "/studio",
            "method": "POST",
            "description": "Trigger FL Studio automation workflows",
            "supported_actions": ["open_session", "switch_audio", "open_project"],
            "example": {"action": "open_session"},
        },
        "voice_commands": {
            "endpoint": "/voice-command",
            "method": "POST",
            "description": "Process natural language voice commands",
            "example": {"command": "create gym note", "use_agent": False},
        },
    }

    return {
        "available_automations": automations,
        "timestamp": datetime.now(),
        "total_endpoints": len(automations),
    }
