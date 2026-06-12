from backend.modules.voice.speech_to_text import SpeechToText
from backend.modules.voice.text_to_speech import TextToSpeech
from backend.services.rag_service import RAGService


class VoiceService:

    @staticmethod
    def configure_voice(rate: int = 175, volume: float = 1.0):
        """Configure voice settings."""
        TextToSpeech.configure(rate=rate, volume=volume)

    @staticmethod
    def listen_and_query(duration: int = 5) -> dict:
        """
        Full voice pipeline:
        1. Record voice from microphone
        2. Transcribe to text
        3. Query RAG
        4. Speak the result

        Returns dict with question and results.
        """

        # Step 1 + 2: Listen and transcribe
        question = SpeechToText.listen(duration=duration)

        if not question:
            TextToSpeech.speak("Sorry, I could not understand. Please try again.")
            return {"status": "error", "message": "Could not transcribe audio"}

        print(f"You asked: {question}")

        # Step 3: Query RAG
        results = RAGService.query(question=question, top_k=3)

        if not results:
            TextToSpeech.speak("Sorry, I could not find any relevant information.")
            return {
                "status": "no_results",
                "question": question,
                "results": []
            }

        # Step 4: Speak first result
        # When LLM is added, this will speak the LLM answer instead
        answer = results[0]
        TextToSpeech.speak(answer)

        return {
            "status": "success",
            "question": question,
            "results": results
        }

    @staticmethod
    def speak(text: str):
        """Speak any text directly."""
        TextToSpeech.speak(text)

    @staticmethod
    def listen(duration: int = 5) -> str:
        """Listen and return transcribed text."""
        return SpeechToText.listen(duration=duration)