"""
Module for managing and displaying available spells in the Command Orchestra.
"""

SPELLS = {
    "📖 Spell Book": {
        "triggers": ["spell book", "list spells", "show spells"],
        "description": "Shows all available spells and their descriptions",
    },
    "💪 New Gym": {
        "triggers": ["new gym", "muscle up"],
        "description": "Creates a new gym directory for workout tracking",
    },
    "📅 New Day": {
        "triggers": ["new day"],
        "description": "Creates a daily note for today",
    },
    "🔮 New Tomorrow": {
        "triggers": ["new day two"],
        "description": "Creates a daily note for tomorrow",
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
