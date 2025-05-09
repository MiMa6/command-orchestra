from speech2action.actions.manager_agent import get_command_from_text


def parse_command(transcript):
    """
    Parses the transcript for known trigger phrases using the manager agent.
    Returns a command dict or None.
    """
    # First try to process with the manager agent
    command = get_command_from_text(transcript)
    if command:
        return command

    # Legacy fallback parsing (for backward compatibility)
    lower = transcript.lower()
    if "spell book" in lower or "list spells" in lower or "show spells" in lower:
        return {"action": "list_spells"}
    if "gym" in lower or "muscle up" in lower:
        return {"action": "create_gym_dir"}
    if "tomorrow" in lower:
        return {"action": "create_tomorrow_note"}
    if "day" in lower:
        return {"action": "create_daily_note"}
    if "running" in lower or "run" in lower:
        return {"action": "create_today_running_note"}
    if "climbing" in lower or "stairs" in lower:
        return {"action": "create_today_stairclimbing_note"}
    if "mobility" in lower:
        return {"action": "create_today_mobility_note"}
    # Add more commands here as needed
    return None
