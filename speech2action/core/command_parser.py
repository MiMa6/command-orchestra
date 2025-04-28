def parse_command(transcript):
    """
    Parses the transcript for known trigger phrases.
    Returns a command dict or None.
    """
    if "new gym" in transcript.lower():
        return {"action": "create_gym_dir"}
    # Add more commands here as needed
    return None
