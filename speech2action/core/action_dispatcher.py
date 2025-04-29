from speech2action.actions.obsidian_automation import (
    create_gym_dir,
    create_daily_note,
    create_tomorrow_note,
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
    else:
        print(f"No automation implemented for action: {action}")
