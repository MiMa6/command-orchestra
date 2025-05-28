# Command Orchestra API Examples

## 🚀 Backend Setup

### Start the Server

```bash
# Option 1: Using the startup script
python run_server.py

# Option 2: Direct uvicorn command
uvicorn speech2action.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Server will be available at:

- **API Base**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

## 📋 API Endpoints

### 1. Health Check

```bash
curl http://localhost:8000/api/v1/health
```

**Response:**

```json
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2024-01-15T10:30:00"
}
```

### 2. Workout Automations (GYM Notes)

#### Running Note

```bash
curl -X POST http://localhost:8000/api/v1/workout \
  -H "Content-Type: application/json" \
  -d '{"workout_type": "running"}'
```

#### Cycling Note

```bash
curl -X POST http://localhost:8000/api/v1/workout \
  -H "Content-Type: application/json" \
  -d '{"workout_type": "cycling"}'
```

#### Mobility Note

```bash
curl -X POST http://localhost:8000/api/v1/workout \
  -H "Content-Type: application/json" \
  -d '{"workout_type": "mobility"}'
```

#### Gym Note

```bash
curl -X POST http://localhost:8000/api/v1/workout \
  -H "Content-Type: application/json" \
  -d '{"workout_type": "gym"}'
```

**Response:**

```json
{
  "success": true,
  "message": "Running automation triggered successfully",
  "timestamp": "2024-01-15T10:30:00",
  "automation_type": "workout_running"
}
```

### 3. Studio Mode (FL Studio)

#### Open Full Session

```bash
curl -X POST http://localhost:8000/api/v1/studio \
  -H "Content-Type: application/json" \
  -d '{"action": "open_session"}'
```

#### Switch Audio Device Only

```bash
curl -X POST http://localhost:8000/api/v1/studio \
  -H "Content-Type: application/json" \
  -d '{"action": "switch_audio"}'
```

#### Launch FL Studio Only

```bash
curl -X POST http://localhost:8000/api/v1/studio \
  -H "Content-Type: application/json" \
  -d '{"action": "open_project"}'
```

**Response:**

```json
{
  "success": true,
  "message": "FL Studio open session automation triggered successfully",
  "timestamp": "2024-01-15T10:30:00",
  "automation_type": "studio_open_session"
}
```

### 4. Daily Notes

#### Create Today's Note

```bash
curl -X POST http://localhost:8000/api/v1/daily-note \
  -H "Content-Type: application/json" \
  -d '{"note_type": "today"}'
```

#### Create Tomorrow's Note

```bash
curl -X POST http://localhost:8000/api/v1/daily-note \
  -H "Content-Type: application/json" \
  -d '{"note_type": "tomorrow"}'
```

### 5. Voice Commands

```bash
curl -X POST http://localhost:8000/api/v1/voice-command \
  -H "Content-Type: application/json" \
  -d '{"command": "create gym note", "use_agent": false}'
```

### 6. List Available Automations

```bash
curl http://localhost:8000/api/v1/automations
```

## 🎯 Frontend Integration Examples

### JavaScript/React Examples

#### Trigger Workout Automation

```javascript
const triggerWorkout = async (workoutType) => {
  try {
    const response = await fetch("http://localhost:8000/api/v1/workout", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        workout_type: workoutType,
      }),
    });

    const result = await response.json();
    console.log("Workout automation result:", result);
    return result;
  } catch (error) {
    console.error("Error triggering workout:", error);
    throw error;
  }
};

// Usage
triggerWorkout("running");
triggerWorkout("cycling");
triggerWorkout("mobility");
triggerWorkout("gym");
```

#### Trigger Studio Mode

```javascript
const triggerStudioMode = async () => {
  try {
    const response = await fetch("http://localhost:8000/api/v1/studio", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        action: "open_session",
      }),
    });

    const result = await response.json();
    console.log("Studio automation result:", result);
    return result;
  } catch (error) {
    console.error("Error triggering studio mode:", error);
    throw error;
  }
};
```

#### React Hook Example

```javascript
import { useState } from "react";

const useAutomation = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const triggerAutomation = async (endpoint, data) => {
    setLoading(true);
    setError(null);

    try {
      const response = await fetch(`http://localhost:8000/api/v1/${endpoint}`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      return result;
    } catch (err) {
      setError(err.message);
      throw err;
    } finally {
      setLoading(false);
    }
  };

  return { triggerAutomation, loading, error };
};

// Usage in component
const WorkoutButtons = () => {
  const { triggerAutomation, loading, error } = useAutomation();

  const handleWorkout = async (type) => {
    try {
      await triggerAutomation("workout", { workout_type: type });
      alert(`${type} automation triggered!`);
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  };

  return (
    <div>
      <button onClick={() => handleWorkout("running")} disabled={loading}>
        Running
      </button>
      <button onClick={() => handleWorkout("cycling")} disabled={loading}>
        Cycling
      </button>
      <button onClick={() => handleWorkout("mobility")} disabled={loading}>
        Mobility
      </button>
      <button onClick={() => handleWorkout("gym")} disabled={loading}>
        Gym
      </button>
    </div>
  );
};
```

## 🔧 Configuration

Make sure your `.env` file is properly configured:

```env
# Obsidian Vault Paths
OBSIDIAN_MAIN_VAULT_PATH=/absolute/path/to/your/main/vault
OBSIDIAN_EXERCISE_VAULT_PATH=/absolute/path/to/your/exercise/vault

# OpenAI API (for voice command processing)
OPENAI_API_KEY=your_openai_api_key

# FL Studio Configuration (optional)
FL_STUDIO_PATH=FL Studio 2024
FL_PROJECT_NAME=DRUMS.flp
FL_AUDIO_DEVICE=AIR 192 4
FL_ASSETS_DIR=assets
WAIT_BETWEEN_TIME=5
```

## 🚦 Error Handling

All endpoints return standardized error responses:

```json
{
  "success": false,
  "message": "Error description",
  "timestamp": "2024-01-15T10:30:00",
  "automation_type": "workout_running"
}
```

Common HTTP status codes:

- `200`: Success
- `400`: Bad request (invalid parameters)
- `422`: Validation error
- `500`: Internal server error

## 🔄 Background Processing

All automation triggers run in the background, so the API responds immediately while the automation executes asynchronously. This ensures your frontend stays responsive.
