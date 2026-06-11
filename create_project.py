import os

folders = [
    "ai-assistant-robot/hardware/chassis",
    "ai-assistant-robot/hardware/wiring",

    "ai-assistant-robot/modules/voice",
    "ai-assistant-robot/modules/meeting",
    "ai-assistant-robot/modules/vision",
    "ai-assistant-robot/modules/navigation",
    "ai-assistant-robot/modules/sound_tracking",
    "ai-assistant-robot/modules/animations",
    "ai-assistant-robot/modules/docking",

    "ai-assistant-robot/memory",

    "ai-assistant-robot/api/routes",

    "ai-assistant-robot/app/src/components",
    "ai-assistant-robot/app/src/pages",
    "ai-assistant-robot/app/src/api",

    "ai-assistant-robot/data/known_faces",
    "ai-assistant-robot/data/meeting_records",
    "ai-assistant-robot/data/logs",

    "ai-assistant-robot/config"
]

files = [
    "ai-assistant-robot/modules/voice/wake_word.py",
    "ai-assistant-robot/modules/voice/stt.py",
    "ai-assistant-robot/modules/voice/tts.py",
    "ai-assistant-robot/modules/voice/llm_agent.py",

    "ai-assistant-robot/modules/meeting/transcription.py",
    "ai-assistant-robot/modules/meeting/diarization.py",
    "ai-assistant-robot/modules/meeting/summarizer.py",
    "ai-assistant-robot/modules/meeting/pdf_export.py",

    "ai-assistant-robot/modules/vision/face_recognition.py",
    "ai-assistant-robot/modules/vision/object_detection.py",

    "ai-assistant-robot/modules/navigation/obstacle_avoidance.py",
    "ai-assistant-robot/modules/navigation/path_planning.py",
    "ai-assistant-robot/modules/navigation/pick_and_place.py",

    "ai-assistant-robot/modules/sound_tracking/tdoa_tracking.py",

    "ai-assistant-robot/modules/animations/eye_display.py",

    "ai-assistant-robot/modules/docking/auto_dock.py",

    "ai-assistant-robot/memory/database.py",
    "ai-assistant-robot/memory/conversation_memory.py",
    "ai-assistant-robot/memory/user_profiles.py",

    "ai-assistant-robot/api/main.py",
    "ai-assistant-robot/api/routes/controls.py",
    "ai-assistant-robot/api/routes/meetings.py",
    "ai-assistant-robot/api/routes/settings.py",
    "ai-assistant-robot/api/websocket.py",

    "ai-assistant-robot/config/settings.yaml",
    "ai-assistant-robot/config/model_config.yaml",

    "ai-assistant-robot/main.py",
    "ai-assistant-robot/requirements.txt",
    "ai-assistant-robot/README.md"
]

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)

# Create files
for file in files:
    with open(file, "w") as f:
        pass

print("✅ AI Assistant Robot project structure created successfully!")