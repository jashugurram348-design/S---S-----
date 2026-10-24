
import speech_recognition as sr
import pyttsx3


class SpeechService:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = None

        # Initialize text-to-speech engine
        try:
            self.engine = pyttsx3.init()
        except Exception as error:
            print(f"Text-to-speech initialization failed: {error}")

    def speech_to_text(self, language="en-IN"):
        """
        Listen through the microphone and convert speech to text.

        Returns a dictionary containing success and text/error.
        """
        try:
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(
                    source, duration=0.5
                )
                print("Listening...")

                audio = self.recognizer.listen(
                    source,
                    timeout=5,
                    phrase_time_limit=10
                )

            text = self.recognizer.recognize_google(
                audio,
                language=language
            )

            return {
                "success": True,
                "text": text
            }

        except sr.WaitTimeoutError:
            return {
                "success": False,
                "error": "No speech detected before timeout."
            }

        except sr.UnknownValueError:
            return {
                "success": False,
                "error": "Could not understand the speech."
            }

        except sr.RequestError:
            return {
                "success": False,
                "error": "Speech recognition service is unavailable."
            }

        except OSError:
            return {
                "success": False,
                "error": "Microphone unavailable or permission denied."
            }

    def text_to_speech(self, text, rate=160):
        """
        Speak the supplied text using the system speech engine.
        """
        if not isinstance(text, str) or not text.strip():
            return {
                "success": False,
                "error": "Please provide text to speak."
            }

        if self.engine is None:
            return {
                "success": False,
                "error": "Text-to-speech engine is unavailable."
            }

        try:
            self.engine.setProperty("rate", rate)
            self.engine.say(text.strip())
            self.engine.runAndWait()

            return {
                "success": True,
                "message": "Speech playback completed."
            }

        except Exception as error:
            return {
                "success": False,
                "error": f"Speech playback failed: {error}"
            }

    def close(self):
        """Release the text-to-speech engine."""
        if self.engine is not None:
            try:
                self.engine.stop()
            except Exception:
                pass


if __name__ == "__main__":
    service = SpeechService()

    try:
        print("1. Speech to text")
        print("2. Text to speech")

        choice = input("Choose an option (1 or 2): ").strip()

        if choice == "1":
            result = service.speech_to_text()
            print(result)

        elif choice == "2":
            text = input("Enter text to speak: ")
            print(service.text_to_speech(text))

        else:
            print("Invalid option.")

    finally:
        service.close()
