"""
Manager Agent using OpenAI Agents SDK for Command Orchestra.
This module implements a manager agent that processes commands and routes them to the appropriate actions.
"""

from typing import Dict, Any, List, Optional
import os

from agents import Agent, Runner, function_tool
from pydantic import BaseModel, Field

from speech2action.actions.obsidian_automation import (
    create_gym_dir,
    create_daily_note,
    create_tomorrow_note,
    create_today_running_note,
    create_today_stairclimbing_note,
    create_today_mobility_note,
)
from speech2action.actions.spell_book import list_spells, SPELLS


# Define our function tools that the agent will use
@function_tool
def create_gym_directory() -> str:
    """
    Creates a new gym directory for workout tracking.
    Use this when the user wants to create a gym directory or track workouts.
    """
    create_gym_dir()
    return "✅ Created a new gym directory for today's workout"


@function_tool
def create_today_note() -> str:
    """
    Creates a daily note for today.
    Use this when the user wants to create a note for today.
    """
    create_daily_note()
    return "✅ Created a daily note for today"


@function_tool
def create_note_for_tomorrow() -> str:
    """
    Creates a daily note for tomorrow.
    Use this when the user wants to create a note for tomorrow.
    """
    create_tomorrow_note()
    return "✅ Created a daily note for tomorrow"


@function_tool
def create_today_running_note_tool() -> str:
    """
    Creates a new running note for today.
    Use this when the user wants to log a run or create a running note.
    """
    create_today_running_note()
    return "✅ Created a new running note for today"


@function_tool
def create_today_stairclimbing_note_tool() -> str:
    """
    Creates a new stairclimbing note for today.
    Use this when the user wants to log stairclimbing or create a stairclimbing note.
    """
    create_today_stairclimbing_note()
    return "✅ Created a new stairclimbing note for today"


@function_tool
def create_today_mobility_note_tool() -> str:
    """
    Creates a new mobility note for today.
    Use this when the user wants to log mobility or create a mobility note.
    """
    create_today_mobility_note()
    return "✅ Created a new mobility note for today"


@function_tool
def show_all_spells() -> str:
    """
    Shows all available spells and their descriptions.
    Use this when the user wants to see a list of available commands or spells.
    """
    list_spells()
    return "✅ Displayed all available spells"


# Create a class for structured output
class CommandResult(BaseModel):
    """Structured output for the manager agent's command processing"""

    action: str = Field(..., description="The specific action that was performed")
    explanation: str = Field(..., description="Brief explanation of what was done")


# Create our manager agent
manager_agent = Agent(
    name="Orchestra Manager",
    instructions="""
    You are the Command Orchestra Manager, an AI that understands and executes commands for the user.
    
    You analyze user input and determine which function to call based on the following trigger phrases:
    - "spell book", "list spells", "show spells" → Show all available spells/commands
    - "gym", "muscle up" → Create a new gym directory for workout tracking
    - "day" → Create a daily note for today
    - "tomorrow" → Create a daily note for tomorrow
    - "running", "run" → Create a new running note for today
    - "climbing", "stairs" → Create a new stairclimbing note for today
    - "mobility" → Create a new mobility note for today
    
    Always respond in a concise, helpful manner after executing the requested action.
    If you're not sure what the user wants, call the show_all_spells() function to help them.
    """,
    tools=[
        create_gym_directory,
        create_today_note,
        create_note_for_tomorrow,
        create_today_running_note_tool,
        create_today_stairclimbing_note_tool,
        create_today_mobility_note_tool,
        show_all_spells,
    ],
    output_type=CommandResult,
)


def process_command(command: str) -> Dict[str, Any]:
    """
    Process a user command using the manager agent.

    Args:
        command: The user command text

    Returns:
        Dict with the result information including success status, action, and message
    """
    try:
        # Run the agent with the user command
        result = Runner.run_sync(manager_agent, command)

        # Extract the result information
        if result and result.final_output:
            return {
                "success": True,
                "action": result.final_output.action,
                "message": result.final_output.explanation,
            }
        else:
            return {
                "success": False,
                "action": None,
                "message": "Failed to process command",
            }
    except Exception as e:
        return {"success": False, "action": None, "message": f"Error: {str(e)}"}


# Update command parser to use manager agent
def get_command_from_text(text: str) -> Dict[str, Any]:
    """
    Process a text command and return the corresponding action.
    This function serves as a bridge between the existing system and our new agent.

    Args:
        text: The user's text command

    Returns:
        Dict with action information
    """
    result = process_command(text)

    if result["success"]:
        # Map the agent's action to the existing action format
        action_map = {
            "create_gym_directory": "create_gym_dir",
            "create_today_note": "create_daily_note",
            "create_note_for_tomorrow": "create_tomorrow_note",
            "create_today_running_note_tool": "create_today_running_note",
            "create_today_stairclimbing_note_tool": "create_today_stairclimbing_note",
            "create_today_mobility_note_tool": "create_today_mobility_note",
            "show_all_spells": "list_spells",
        }

        # Get the corresponding action name or use the original if not found
        action_name = action_map.get(result["action"], result["action"])

        return {"action": action_name, "result": result}
    else:
        # Fallback to None if the agent couldn't process the command
        return None
