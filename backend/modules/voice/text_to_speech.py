import pyttsx3


class TextToSpeech:

    @staticmethod
    def speak(text: str):
        """
        Converts text to speech and plays it.
        Creates a fresh engine every time to avoid event loop conflicts.
        """
        print(f"Robot speaking: {text}")
        engine = pyttsx3.init()
        engine.setProperty("rate", 175)
        engine.setProperty("volume", 1.0)
        engine.say(text)
        engine.runAndWait()
        engine.stop()

    @staticmethod
    def speak_streaming(text: str):
        """Speaks sentence by sentence."""
        sentences = text.split(".")
        for sentence in sentences:
            sentence = sentence.strip()
            if sentence:
                TextToSpeech.speak(sentence)