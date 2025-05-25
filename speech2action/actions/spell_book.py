"""
Module for managing and displaying available spells in the Command Orchestra.
"""

SPELLS = {
    "📖 Spell Book": {
        "triggers": ["spell book", "list spells", "show spells"],
        "description": "Shows all available spells and their descriptions",
    },
    "💪 Gym": {
        "triggers": ["gym", "muscle up"],
        "description": "Creates a new gym directory for workout tracking",
    },
    "📅 Day": {
        "triggers": ["day"],
        "description": "Creates a daily note for today",
    },
    "🔮 Tomorrow": {
        "triggers": ["tomorrow"],
        "description": "Creates a daily note for tomorrow",
    },
    "🏃 Running": {
        "triggers": ["running", "run"],
        "description": "Creates a new running note for today",
    },
    "🧗 Stairclimbing": {
        "triggers": ["climbing", "stairs"],
        "description": "Creates a new stairclimbing note for today",
    },
    "🧘 Mobility": {
        "triggers": ["mobility"],
        "description": "Creates a new mobility note for today",
    },
    "🎹 Studio": {
        "triggers": ["studio", "fl", "music"],
        "description": "Launches FL Studio and opens the configured project.",
    },
    "🚴 Cycling": {
        "triggers": ["cycling", "bike"],
        "description": "Creates a new cycling note for today",
    },
}


def list_spells():
    """
    Displays all available spells and their descriptions in a formatted way.
    """
    print("\n🪄 Available Spells in Command Orchestra 📚\n")
    print("=" * 50)

    for spell_name, spell_info in SPELLS.items():
        triggers = " | ".join([f'"{t}"' for t in spell_info["triggers"]])
        print(f"\n{spell_name}")
        print("-" * len(spell_name))
        print(f"Triggers: {triggers}")
        print(f"Description: {spell_info['description']}")

    print("\n" + "=" * 50)
