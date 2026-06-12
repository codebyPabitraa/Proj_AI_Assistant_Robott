from faster_whisper import WhisperModel
import sounddevice as sd
import numpy as np
import io
import wave


class SpeechToText:

    _model = WhisperModel("small", device="cpu", compute_type="int8")

    @staticmethod
    def record_audio(duration: int = 5, sample_rate: int = 16000) -> np.ndarray:
        print(f"Recording for {duration} seconds...")
        audio = sd.rec(
            int(duration * sample_rate),
            samplerate=sample_rate,
            channels=1,
            dtype="float32",
            device=1
        )
        sd.wait()
        print("Recording complete.")
        return audio

    @staticmethod
    def transcribe_audio(audio: np.ndarray, sample_rate: int = 16000) -> str:
        buffer = io.BytesIO()
        with wave.open(buffer, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes((audio * 32767).astype(np.int16).tobytes())
        buffer.seek(0)
        segments, _ = SpeechToText._model.transcribe(buffer, language="en")
        text = " ".join([segment.text for segment in segments])
        return text.strip()

    @staticmethod
    def listen(duration: int = 5) -> str:
        audio = SpeechToText.record_audio(duration=duration)
        return SpeechToText.transcribe_audio(audio)