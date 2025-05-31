import asyncio
from speech2action.actions.flstudio_automation import open_drum_session
from speech2action.actions.obsidian_automation import (
    create_gym_dir,
    create_daily_note,
    create_tomorrow_note,
    create_today_running_note,
    create_today_stairclimbing_note,
    create_today_mobility_note,
    create_today_cycling_note,
)
from speech2action.actions.spell_book import list_spells
from speech2action.actions.manager_agent import process_command, process_command_async


async def dispatch_action_async(command, use_agent=False):
    """
    Async version of dispatch_action that properly handles agent operations.

    Args:
        command: The parsed command dict or command text
        use_agent: Whether to use the OpenAI Agents SDK (default: False)
    """
    if use_agent:
        # Use the async version for agent processing
        if isinstance(command, str):
            result = await process_command_async(command)
        elif isinstance(command, dict) and "result" in command:
            result = command["result"]
        else:
            action = command.get("action", "")
            result = await process_command_async(action)

        if result.get("success"):
            print(result["message"])
        else:
            print(result.get("message", "No recognized command. Try again."))
        return

    # For traditional mode, run in thread pool to avoid blocking
    loop = asyncio.get_event_loop()
    await loop.run_in_executor(None, _dispatch_traditional, command)


def _dispatch_traditional(command):
    """Helper function to handle traditional command dispatch."""
    # Check if result is already included (from manager agent)
    if isinstance(command, dict) and "result" in command:
        result = command["result"]
        print(result["message"])
        return

    # Traditional action dispatch
    action = command.get("action")
    if action == "list_spells":
        list_spells()
    elif action == "create_gym_dir":
        create_gym_dir()
    elif action == "create_daily_note":
        create_daily_note()
    elif action == "create_tomorrow_note":
        create_tomorrow_note()
    elif action == "create_today_running_note":
        create_today_running_note()
    elif action == "create_today_stairclimbing_note":
        create_today_stairclimbing_note()
    elif action == "create_today_mobility_note":
        create_today_mobility_note()
    elif action == "create_today_cycling_note":
        create_today_cycling_note()
    elif action == "spell_studio" or action == "open_drum_session":
        open_drum_session()
    else:
        print(f"No automation implemented for action: {action}")


def dispatch_action(command, use_agent=False):
    """
    Dispatches the command to the appropriate automation function.

    Args:
        command: The parsed command dict or command text
        use_agent: Whether to use the OpenAI Agents SDK (default: False)
    """
    # If use_agent is True, we need to run this in an async context
    if use_agent:
        # For agent mode, create a new event loop in a thread
        def run_agent():
            try:
                # Create a new event loop for this thread
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)

                if isinstance(command, str):
                    # Run the sync version since we have a clean event loop
                    result = process_command(command)
                elif isinstance(command, dict) and "result" in command:
                    result = command["result"]
                else:
                    action = command.get("action", "")
                    result = process_command(action)

                if result.get("success"):
                    print(result["message"])
                else:
                    print(result.get("message", "No recognized command. Try again."))

            finally:
                loop.close()

        # Run in a separate thread
        import threading

        thread = threading.Thread(target=run_agent)
        thread.start()
        thread.join()
        return

    # Traditional mode - run directly
    _dispatch_traditional(command)
