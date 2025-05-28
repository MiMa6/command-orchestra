# 🎻 Command Orchestra 🪄

Welcome to your **AI Agent Automation Playground**!

## 🧬 Vision

Build your own living operating system: command your AI Agent with your voice (or text), and watch it orchestrate workflows, open apps, and automate your creative rituals. Speech-2-Action! 🗣️✨

## 🚀 FastAPI Backend

The Command Orchestra includes FastAPI backend that allows you to trigger automations from your frontend applications!

<img src="public/assets/images/Backend-28-5-2025.png" alt="Command Orchestra Frontend Screenshot" width="500">


**API will be available at:**

- 🌐 **Backend**: http://localhost:8000
- 📚 **API Docs**: http://localhost:8000/docs
- 🔄 **Health Check**: http://localhost:8000/api/v1/health

### API Endpoints

- `POST /api/v1/workout` - Trigger workout automations (running, cycling, mobility, gym)
- `POST /api/v1/studio` - Launch FL Studio and configure audio
- `POST /api/v1/daily-note` - Create daily notes in Obsidian
- `POST /api/v1/voice-command` - Process natural language commands
- `GET /api/v1/automations` - List all available automations

See [API_EXAMPLES.md](API_EXAMPLES.md) for detailed usage examples and frontend integration code.

## 📦 Project Structure

```text
Command-Orchestra/
├── .venv/
├── requirements.txt
├── README.md
├── API_EXAMPLES.md               # API usage examples and frontend integration
├── run_server.py                 # FastAPI server startup script
└── speech2action/
    ├── main.py                   # Original CLI application
    ├── api/                      # NEW: FastAPI backend
    │   ├── __init__.py
    │   ├── main.py              # FastAPI application
    │   ├── routes.py            # API endpoints
    │   ├── models.py            # Pydantic models
    │   └── middleware.py        # CORS and logging middleware
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
## Frontend Repository

🔗 **Frontend**: [Command Orchestra Frontend](https://github.com/MiMa6/command-orchestra-frontend) - The React frontend interface for voice and manual trigger command interaction


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

## 🎮 Usage

### Option 1: FastAPI Backend (Recommended)

```bash
# Start the API server
python run_server.py

# Server runs at http://localhost:8000
# Use with your frontend or make direct API calls
```

### Option 2: Original CLI Mode

```bash
# Run the original CLI application
python -m speech2action.main
```

> Play, experiment, and extend — your digital symphony awaits! 🎶
