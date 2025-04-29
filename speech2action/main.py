from speech2action.core.voice_listener import listen_for_command
from speech2action.core.command_parser import parse_command
from speech2action.core.action_dispatcher import dispatch_action
from speech2action.actions.manager_agent import process_command
from speech2action.config import settings


def main():
    """
    Main function that handles the command orchestration loop.
    """
    print("🎻 Speech-2-Action Orchestra 🪄")
    print("\nChoose your mode:")
    print("1. Standard mode (traditional parser)")
    print("2. Agent mode (OpenAI Agents SDK)")

    mode = input("Select mode (1 or 2): ")
    use_agent = mode == "2"

    if use_agent:
        print("\n🤖 Using OpenAI Agents SDK Manager\n")
    else:
        print("\n🧩 Using Traditional Command Parser\n")

    print("Type your command (spell) or 'exit' to quit:")
    print("To show all available spells, say 'list spells'")

    while True:
        # For now, use text input. Replace with real voice input later.
        transcript = listen_for_command()

        if transcript.lower() == "exit":
            print("Goodbye!")
            break

        # Switch between agent and traditional mode
        if use_agent:
            # Direct use of the agent for processing
            result = process_command(transcript)
            if result["success"]:
                print(result["message"])
            else:
                print(result["message"] or "No recognized command. Try again.")
        else:
            # Traditional processing path
            command = parse_command(transcript)
            if command:
                dispatch_action(command)
            else:
                print("No recognized command. Try again.")


if __name__ == "__main__":
    main()
