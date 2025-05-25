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


def dispatch_action(command):
    """
    Dispatches the command to the appropriate automation function.
    """
    # Check if result is already included (from manager agent)
    if isinstance(command, dict) and "result" in command:
        result = command["result"]
        # Just print the success message from the agent
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
