from fastapi import APIRouter
from pydantic import BaseModel
from backend.services.voice_service import VoiceService

router = APIRouter()


# --- Listen and Query Endpoint ---
@router.post("/listen")
def listen_and_query(duration: int = 5):
    """
    Records voice from microphone.
    Transcribes to text.
    Queries RAG.
    Speaks the answer.
    """
    result = VoiceService.listen_and_query(duration=duration)
    return result


# --- Text to Speech Endpoint ---
class SpeakRequest(BaseModel):
    text: str


@router.post("/speak")
def speak(request: SpeakRequest):
    """
    Converts text to speech.
    Robot speaks the given text.
    """
    VoiceService.speak(request.text)
    return {"status": "success", "spoken": request.text}


# --- Transcribe Only Endpoint ---
@router.post("/transcribe")
def transcribe(duration: int = 5):
    """
    Records voice and returns transcribed text.
    Does not query RAG or speak.
    """
    text = VoiceService.listen(duration=duration)
    return {"transcribed_text": text}