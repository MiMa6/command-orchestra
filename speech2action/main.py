from speech2action.core.voice_listener import listen_for_command
from speech2action.core.command_parser import parse_command
from speech2action.core.action_dispatcher import dispatch_action
from speech2action.config import settings


def main():
    print("🎻 Speech-2-Action Orchestra 🪄")
    print("Type your command (spell) or 'exit' to quit:")
    while True:
        # For now, use text input. Replace with real voice input later.
        transcript = listen_for_command()
        if transcript.lower() == "exit":
            print("Goodbye!")
            break
        command = parse_command(transcript)
        if command:
            dispatch_action(command)
        else:
            print("No recognized command. Try again.")


if __name__ == "__main__":
    main()
