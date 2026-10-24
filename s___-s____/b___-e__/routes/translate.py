
from flask import Blueprint, request, jsonify

translate_bp = Blueprint("translate", __name__, url_prefix="/api/translate")


# Demo phrase mapping.
# Replace or extend this with a real sign-language translation model.
DEMO_TRANSLATIONS = {
    "hello": "Hello",
    "how are you": "How are you?",
    "thank you": "Thank you",
    "good morning": "Good morning",
    "help me": "I need help",
    "i love you": "I love you",
    "yes": "Yes",
    "no": "No",
    "sorry": "I'm sorry",
}


@translate_bp.route("/", methods=["POST"])
def translate_text():
    data = request.get_json(silent=True) or {}

    text = data.get("text", "").strip()
    mode = data.get("mode", "text").strip().lower()

    if not text:
        return jsonify({
            "success": False,
            "error": "Please provide text to translate."
        }), 400

    if mode not in ("text", "speech", "sign"):
        return jsonify({
            "success": False,
            "error": "Mode must be text, speech, or sign."
        }), 400

    # Demo text mapping, not actual sign-language recognition.
    translated_text = DEMO_TRANSLATIONS.get(
        text.lower(),
        f"Demo translation: {text}"
    )

    return jsonify({
        "success": True,
        "original_text": text,
        "translated_text": translated_text,
        "mode": mode,
        "is_demo": True,
        "message": (
            "Demo response only. A trained sign-language model "
            "is required for real sign recognition or translation."
        )
    }), 200


@translate_bp.route("/health", methods=["GET"])
def translate_health():
    return jsonify({
        "success": True,
        "service": "translation",
        "status": "running"
    }), 200
