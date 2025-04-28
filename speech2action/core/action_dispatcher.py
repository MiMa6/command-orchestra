from speech2action.actions.obsidian_automation import (
    create_gym_dir,
    create_daily_note,
    create_tomorrow_note,
)


def dispatch_action(command):
    """
    Dispatches the command to the appropriate automation function.
    """
    action = command.get("action")
    if action == "create_gym_dir":
        create_gym_dir()
    elif action == "create_daily_note":
        create_daily_note()
    elif action == "create_tomorrow_note":
        create_tomorrow_note()
    else:
        print(f"No automation implemented for action: {action}")
