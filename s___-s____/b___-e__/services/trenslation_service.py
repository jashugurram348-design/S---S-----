
from deep_translator import GoogleTranslator


class TranslationService:
    def __init__(self):
        # Supported language codes for text translation
        self.supported_languages = {
            "english": "en",
            "telugu": "te",
            "hindi": "hi",
            "tamil": "ta",
            "kannada": "kn",
            "malayalam": "ml",
            "spanish": "es",
            "french": "fr",
        }

        # Demo phrases only; not a real sign-language model
        self.sign_phrases = {
            "hello": "Hello",
            "thank you": "Thank you",
            "how are you": "How are you?",
            "help me": "I need help",
            "good morning": "Good morning",
            "i love you": "I love you",
        }

    def translate_text(
        self,
        text,
        source_language="english",
        target_language="telugu"
    ):
        """Translate text between supported spoken languages."""

        if not isinstance(text, str) or not text.strip():
            return {
                "success": False,
                "error": "Please provide text to translate."
            }

        source = self.supported_languages.get(
            source_language.lower()
        )
        target = self.supported_languages.get(
            target_language.lower()
        )

        if not source or not target:
            return {
                "success": False,
                "error": "Unsupported source or target language.",
                "supported_languages": list(
                    self.supported_languages.keys()
                )
            }

        if source == target:
            return {
                "success": True,
                "original_text": text.strip(),
                "translated_text": text.strip(),
                "source_language": source_language,
                "target_language": target_language
            }

        try:
            translated = GoogleTranslator(
                source=source,
                target=target
            ).translate(text.strip())

            return {
                "success": True,
                "original_text": text.strip(),
                "translated_text": translated,
                "source_language": source_language,
                "target_language": target_language
            }

        except Exception:
            return {
                "success": False,
                "error": (
                    "Translation failed. Check your internet "
                    "connection and try again."
                )
            }

    def get_demo_sign_phrase(self, phrase):
        """Return a matching demo phrase, if available."""

        if not isinstance(phrase, str) or not phrase.strip():
            return {
                "success": False,
                "error": "Please provide a phrase."
            }

        result = self.sign_phrases.get(phrase.strip().lower())

        if result is None:
            return {
                "success": False,
                "error": "Phrase is not available in the demo."
            }

        return {
            "success": True,
            "original_text": phrase.strip(),
            "translated_text": result,
            "is_demo": True
        }

    def get_supported_languages(self):
        """Return available language names and language codes."""

        return {
            name: code
            for name, code in self.supported_languages.items()
        }


if __name__ == "__main__":
    service = TranslationService()

    result = service.translate_text(
        "Hello, how are you?",
        source_language="english",
        target_language="telugu"
    )
    print(result)

    print(service.get_supported_languages())
