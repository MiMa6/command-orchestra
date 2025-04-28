def parse_command(transcript):
    """
    Parses the transcript for known trigger phrases.
    Returns a command dict or None.
    """
    lower = transcript.lower()
    if "new gym" in lower or "muscle up" in lower:
        return {"action": "create_gym_dir"}
    if "new day two" in lower:
        return {"action": "create_tomorrow_note"}
    if "new day" in lower:
        return {"action": "create_daily_note"}
    # Add more commands here as needed
    return None
