# 🎻 Command Orchestra 🪄

Welcome to your **AI Agent Automation Playground**!

## 🚀 Vision

Build your own living operating system: command your AI Agent with your voice (or text), and watch it orchestrate workflows, open apps, and automate your creative rituals. Speech-2-Action! 🗣️✨

## 🪄 Spells (Commands)

| Spell                                          | What it Does                                                                                                             |
| ---------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------ |
| `Spell book`            | Shows all available spells and their descriptions                                                                         |
| `Studio`                                       | Launch FL Studio and automatically open your drum project for a music session                                           |
| `New day`                                      | Create today's daily note in your main Obsidian vault, using the daily template if available                                |
| `Tomorrow`                                     | Create tomorrow's daily note in your main Obsidian vault, using the daily template if available                           |
| `Gym`                                          | Create a new gym obsidian directory for today in your exercise vault, cycling exercise groups and copying previous notes |
| `Running`                                      | Create a new running note for today in your exercise vault, copying the latest note content and updating the date           |
| `Stairs`                                       | Create a new stairclimbing note for today in your exercise vault, copying the latest note content and updating the date  |
| `Cycling`                                      | Create a new cycling note for today in your exercise vault, copying the latest note content and updating the date           |

**Daily notes are created at:**

```
<OBSIDIAN_MAIN_VAULT_PATH>/📆/<year-month>/<year-month-day>.md
```

**Template location:**

```
<OBSIDIAN_MAIN_VAULT_PATH>/Templates/Daily Note Template.md
```

---

## 📦 Project Structure

```text
Command-Orchestra/
├── .venv/
├── requirements.txt
├── README.md
└── speech2action/
    ├── main.py
    ├── actions/
    │   ├── spell_book.py           # Spell definitions and triggers
    │   ├── manager_agent.py        # OpenAI Agents implementation
    │   ├── obsidian_automation.py  # Obsidian note automation
    │   ├── flstudio_automation.py  # FL Studio automation
    │   └── __init__.py
    ├── core/
    │   ├── command_parser.py       # Command parsing logic
    │   ├── action_dispatcher.py    # Dispatches actions to automations
    │   ├── voice_listener.py       # Voice/text input handler
    │   └── __init__.py
    ├── config/
    │   ├── settings.py             # Environment/config management
    │   └── __init__.py
    └── __pycache__/
```

## 🛠️ Setup

1. **Clone repo & create venv:**
   ```bash
   git clone <repo-url>
   cd Command-Orchestra
   python3 -m venv .venv
   source .venv/bin/activate
   ```
2. **Install requirements:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Configure your Obsidian vault path in `.env`:**
   ```env
   OBSIDIAN_MAIN_VAULT_PATH=/absolute/path/to/your/main/vault
   OBSIDIAN_EXERCISE_VAULT_PATH=/absolute/path/to/your/exercise/vault
   OPENAI_API_KEY=your_openai_api_key  # Required for Agent mode
   ```
4. **Run the app from root:**
   ```bash
   python -m speech2action.main
   ```
   > Play, experiment, and extend — your digital symphony awaits! 🎶
