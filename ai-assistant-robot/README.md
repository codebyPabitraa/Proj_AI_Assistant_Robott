# AI Assistant Robot - Local Robot Software

This directory contains the local robot software that runs on the Raspberry Pi 4. It handles voice interaction, autonomous navigation, meeting management, and hardware control.

---

## 📌 Quick Start (5 minutes)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Start the robot
python main.py
```

**✅ Result:** Robot starts listening for "hey robot" wake word

---

## 🏗️ Directory Structure

```
ai-assistant-robot/
│
├── main.py                      # Entry point - starts all modules
├── requirements.txt             # Python dependencies
├── README.md                    # This file
│
├── api/                         # FastAPI Web Server
│   ├── main.py                  # FastAPI app, REST endpoints
│   ├── websocket.py             # WebSocket manager for real-time updates
│   └── routes/
│       ├── controls.py          # Motor & navigation commands
│       ├── meetings.py          # Meeting start/stop/export
│       └── settings.py          # Robot configuration endpoints
│
├── config/                      # Configuration Files
│   ├── settings.yaml            # Main robot settings
│   ├── model_config.yaml        # LLM, Whisper, TTS models
│   └── hardware_config.yaml     # GPIO pins, motor specs
│
├── data/                        # Runtime Data
│   ├── logs/                    # Log files
│   │   ├── robot.log            # Main robot log
│   │   ├── api.log              # API server log
│   │   └── meeting.log          # Meeting processing log
│   ├── meeting_records/         # Meeting transcripts & reports
│   │   └── {date}/
│   │       ├── meeting_{id}.db
│   │       ├── meeting_{id}.wav
│   │       ├── meeting_{id}_transcript.md
│   │       └── meeting_{id}_report.pdf
│   └── known_faces/             # Face recognition database (optional)
│
├── hardware/                    # Hardware Configuration
│   ├── chassis/
│   │   ├── main_frame.step      # CAD models
│   │   ├── motor_mount.step
│   │   └── bom.csv              # Bill of materials
│   └── wiring/
│       ├── power_distribution.txt
│       └── gpio_pinout.md
│
├── memory/                      # Robot Memory & Context
│   ├── conversation_memory.py   # Conversation history management
│   ├── database.py              # SQLite database interface
│   └── user_profiles.py         # User data & preferences
│
└── modules/                     # Functional Modules (see below)
    ├── animations/
    │   ├── eye_display.py       # OLED eye control
    │   └── expressions.py       # Emotional expressions
    │
    ├── docking/
    │   └── auto_dock.py         # Autonomous docking system
    │
    ├── meeting/
    │   ├── transcription.py     # Whisper transcription
    │   ├── diarization.py       # Speaker identification
    │   ├── summarizer.py        # Meeting summarization
    │   └── pdf_export.py        # PDF report generation
    │
    ├── navigation/
    │   ├── path_planning.py     # A* pathfinding
    │   ├── obstacle_avoidance.py # Safety checks
    │   └── motor_controller.py  # Motor control via GPIO
    │
    └── voice/
        ├── wake_word.py         # Porcupine wake word detection
        ├── stt.py               # OpenAI Whisper STT
        ├── llm_agent.py         # LLaMA 3.2 via Ollama
        ├── tts.py               # Piper text-to-speech
        └── audio_utils.py       # Audio processing utilities
```

---

## 🔧 Installation Guide

### Prerequisites

✅ Raspberry Pi 4 (8GB recommended)
✅ Python 3.9+
✅ 20GB+ free disk space
✅ USB microphone
✅ USB speaker or 3.5mm jack

### Step 1: System Dependencies

```bash
# Update package lists
sudo apt update && sudo apt upgrade -y

# Install system packages
sudo apt install -y \
    python3-pip \
    python3-dev \
    libportaudio2 \
    portaudio19-dev \
    libasound2-dev \
    ffmpeg \
    git

# Test installation
python3 --version  # Should be 3.9+
```

### Step 2: Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
# On Windows: venv\Scripts\activate

# Verify activation (should show "venv" prefix in terminal)
python --version
```

### Step 3: Install Python Packages

```bash
# Install required packages
pip install -r requirements.txt

# Verify critical packages
python -c "import whisper; print('✓ Whisper')"
python -c "import pyaudio; print('✓ PyAudio')"
python -c "import requests; print('✓ Requests')"
```


### Step 5: Install Local LLM (Ollama)

```bash
# Option A: Ollama (Recommended)
curl -fsSL https://ollama.ai/install.sh | sh

# Download LLaMA 3.2 3B (Quantized for Pi)
ollama pull llama3.2:3b

# Verify
ollama list  # Should show llama3.2:3b

# Keep Ollama running in background
ollama serve &
```

### Step 6: Configure Hardware

```bash
# Test microphone
arecord -l

# Test speaker
aplay /usr/share/sounds/alsa/Front_Left.wav

# Test GPIO (if motors connected)
python -c "import RPi.GPIO as GPIO; print(f'GPIO version: {GPIO.VERSION}')"

# Test I2C (if sensors connected)
sudo i2cdetect -y 1
```

### Step 7: Run the Robot

```bash
# Terminal 1: Start Ollama
ollama serve

# Terminal 2: Start Robot
source venv/bin/activate
python main.py

# You should see:
# [Main] Starting AI Assistant Robot...
# [Voice] Listening for wake word...
```

---

## 🎮 Usage Guide

### Voice Commands

After hearing "Listening...", speak commands:

```
"Hey robot, what time is it?"
"Navigate to the kitchen"
"Start a meeting called review"
"Go dock yourself"
"What's the weather?"
"How many people are here?"
```

### API Endpoints

Robot runs FastAPI server on `http://localhost:8000`

**Telemetry:**
```bash
curl http://localhost:8000/api/status
# Returns: {state, battery, position, heading}
```

**Navigation:**
```bash
curl -X POST http://localhost:8000/api/controls/navigate \
  -H "Content-Type: application/json" \
  -d '{"target_x": 5.0, "target_y": 3.0}'
```

**Start Meeting:**
```bash
curl -X POST http://localhost:8000/api/meetings/start \
  -H "Content-Type: application/json" \
  -d '{"title": "Team Standup"}'
```

**Dock:**
```bash
curl -X POST http://localhost:8000/api/controls/dock
```

### Python API (Direct)

```python
from modules.voice.llm_agent import ask_llm
from modules.voice.tts import speak
from modules.navigation.path_planning import PathPlanner

# Ask LLM
response = ask_llm("What is 2 + 2?")
print(response)

# Speak response
speak(response)

# Navigate
planner = PathPlanner(200, 200, cell_size=0.1)
path = planner.plan((0, 0), (5, 5))
for waypoint in path:
    print(f"Moving to {waypoint}")
```

---

## ⚙️ Configuration

### config/settings.yaml

Main robot configuration:

```yaml
robot:
  name: "My Robot"
  id: "robot_001"
  debug: false

voice:
  wake_word: "hey robot"
  stt_model: "base"           # tiny, base, small, medium
  
navigation:
  max_speed: 0.5              # meters/second
  grid_resolution: 0.1        # 10cm cells

docking:
  enabled: true
  battery_threshold: 20       # % to trigger auto-dock
  dock_location: [0, 0]
```

### config/model_config.yaml

AI model settings:

```yaml
whisper:
  model: "base"               # Larger = slower but more accurate
  device: "cpu"               # cuda if GPU available

ollama:
  base_url: "http://localhost:11434"
  model: "llama3.2:3b"
  temperature: 0.7

piper:
  model: "en_US-lessac-medium"
  sample_rate: 22050
```

### Environment Variables

Create `.env` file:

```bash
export LOG_LEVEL="INFO"
export ROBOT_ID="robot_001"
export OLLAMA_HOST="http://localhost:11434"
export CLOUD_ENABLED="false"
export DEBUG_MODE="false"
```

---

## 📊 Modules Overview

### Voice Module (`modules/voice/`)

Handles speech interaction:

```python
from modules.voice.wake_word import listen_for_wake_word
from modules.voice.stt import listen_and_transcribe
from modules.voice.llm_agent import ask_llm
from modules.voice.tts import speak

def voice_loop():
    def on_wake_word():
        text = listen_and_transcribe(duration=5)
        response = ask_llm(text)
        speak(response)
    
    listen_for_wake_word(on_wake_word)

voice_loop()
```

**Components:**
- `wake_word.py` — Porcupine wake word detection
- `stt.py` — Whisper speech-to-text
- `llm_agent.py` — LLaMA LLM inference
- `tts.py` — Piper text-to-speech
- `audio_utils.py` — Audio processing

### Navigation Module (`modules/navigation/`)

Handles autonomous movement:

```python
from modules.navigation.path_planning import PathPlanner
from modules.navigation.obstacle_avoidance import ObstacleAvoidance
from modules.navigation.motor_controller import MotorController

planner = PathPlanner(200, 200, cell_size=0.1)
avoidance = ObstacleAvoidance(safety_radius=0.3)
motor = MotorController(motor_pins={...})

path = planner.plan((0, 0), (10, 10))
for waypoint in path:
    if avoidance.is_safe(waypoint):
        motor.drive_to_waypoint(waypoint)
```

**Components:**
- `path_planning.py` — A* algorithm
- `obstacle_avoidance.py` — Safety checks
- `motor_controller.py` — GPIO motor control

### Docking Module (`modules/docking/`)

Autonomous charging:

```python
from modules.docking.auto_dock import AutoDockingSystem

docker = AutoDockingSystem(dock_location=(0, 0))
if docker.should_dock():
    success = docker.initiate_docking()
```

**Features:**
- IR beacon detection
- Camera alignment
- Inductive charging
- Battery monitoring

### Meeting Module (`modules/meeting/`)

Transcription & summarization:

```python
from modules.meeting.transcription import MeetingTranscriber
from modules.meeting.summarizer import MeetingSummarizer

transcriber = MeetingTranscriber()
summarizer = MeetingSummarizer()

# Record meeting
while meeting_active:
    audio_chunk = get_audio()
    transcriber.transcribe_chunk(audio_chunk)

# Generate report
report = summarizer.generate_meeting_report(
    transcriber.get_transcript()
)
```

**Features:**
- Real-time transcription
- Speaker diarization
- Abstractive summarization
- PDF export

---

## 🧠 Memory System

### Conversation History

Managed by the memory module and stored in SQLite via the project database interface:

```python
from memory.database import get_history, save_turn

# Get conversation history
history = get_history(user_id=1, limit=10)
for turn in history:
    print(f"{turn['role']}: {turn['message']}")

# Save new turn
save_turn(user_id=1, user_msg="Hello", bot_reply="Hi!")
```

### User Profiles

Store user preferences:

```python
from memory.user_profiles import UserProfile

profile = UserProfile.load(user_id=1)
print(f"Name: {profile.name}")
print(f"Preferences: {profile.preferences}")
```

---

## 🚨 Troubleshooting

### Import Errors

```
ModuleNotFoundError: No module named 'whisper'
```

**Solution:**
```bash
pip install openai-whisper
pip install -r requirements.txt
```

### Ollama Not Found

```
ollama: command not found
```

**Solution:**
```bash
curl -fsSL https://ollama.ai/install.sh | sh
ollama pull llama3.2:3b
ollama serve &
```

### Microphone Issues

```
[Voice] No microphone input detected
```

**Solution:**
```bash
# List audio devices
arecord -l

# Update device index in modules/voice/stt.py:
# input_device_index = 2  (replace with your mic's index)
```

### High Memory Usage

```
MemoryError: Unable to allocate 1.2GB
```

**Solutions:**
1. Use smaller models: `whisper tiny` instead of `base`
2. Reduce LLM context size
3. Close other applications
4. Upgrade to 16GB Pi or Jetson Orin

### API Port Already in Use

```
OSError: [Errno 98] Address already in use
```

**Solution:**
```bash
# Find process using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or use different port
python api/main.py --port 8001
```

---

## 📊 Performance Benchmarks

On Raspberry Pi 4 (8GB):

| Component | Latency | Model |
|-----------|---------|-------|
| Wake word | 50-100ms | Porcupine (on-device) |
| STT | 2-5s | Whisper base |
| LLM inference | 3-8s | LLaMA 3.2 3B Q4 |
| TTS synthesis | 1-3s | Piper medium |
| Navigation loop | 100ms | A* + obstacle check |
| Motor control | 10-50ms | GPIO PWM |
| API response | 50-100ms | FastAPI |

**Total voice interaction:** ~10-15 seconds

---

## 🔄 Main Loop Flow

```
main.py
  ├─ Initialize modules
  ├─ Start FastAPI server (port 8000)
  ├─ Start WebSocket manager
  └─ Main voice loop:
      ├─ Listen for wake word
      ├─ Record audio (5 seconds)
      ├─ Transcribe with Whisper
      ├─ Send to LLaMA for response
      ├─ Synthesize response with Piper
      ├─ Play audio
      ├─ Save conversation to database
      └─ Loop back to step 1
```

---

## 📝 Logging

Logs are stored in `data/logs/`:

```bash
# View real-time logs
tail -f data/logs/robot.log

# Check API logs
tail -f data/logs/api.log

# Check meeting processing logs
tail -f data/logs/meeting.log

# Search for errors
grep ERROR data/logs/robot.log
```

Log levels (in order of verbosity):
- `DEBUG` — Detailed debugging info
- `INFO` — General information (default)
- `WARNING` — Warning messages
- `ERROR` — Error messages
- `CRITICAL` — Critical failures

Change log level in `config/settings.yaml`:
```yaml
logging:
  level: "INFO"  # or DEBUG, WARNING, etc.
```

---

## 🧪 Testing

```bash
# Run all tests
pytest tests/ -v

# Run specific test
pytest tests/test_voice.py::test_wake_word -v

# Run with coverage
pytest --cov=modules tests/

# Run integration tests
pytest tests/integration/ -v
```

---

## 📚 Learn More

- **Voice Module:** See [Module 01](../System%20Design/1.voice%20assistant.md)
- **Navigation:** See [Module 05](../System%20Design/5.navigation%20and%20path%20planning.md)
- **Docking:** See [Module 07](../System%20Design/7.autonomous%20docking.md)
- **API:** See [Module 10](../System%20Design/10.api%20and%20system%20integration.md)
- **Meetings:** See [Module 12](../System%20Design/12.meeting%20management%20and%20transcription.md)

---

## 🤝 Contributing

1. Create feature branch: `git checkout -b feature/my-feature`
2. Make changes in modules
3. Add tests in `tests/`
4. Run: `pytest` & `black modules/ api/`
5. Commit: `git commit -m "feat: my feature"`
6. Push & create PR

---

**Happy building! 🚀**
