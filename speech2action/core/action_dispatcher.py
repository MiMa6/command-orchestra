from speech2action.actions.obsidian_automation import create_gym_dir


def dispatch_action(command):
    """
    Dispatches the command to the appropriate automation function.
    """
    action = command.get("action")
    if action == "create_gym_dir":
        create_gym_dir()
    else:
        print(f"No automation implemented for action: {action}")
