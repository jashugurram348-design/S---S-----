
"""
SignSpeak - Sign Language Dictionary API

Provides dictionary entries and search endpoints
for the SignSpeak Flask backend.
"""

from flask import Blueprint, jsonify, request

dictionary_bp = Blueprint("dictionary", __name__, url_prefix="/api/dictionary")


# Starter dictionary data.
# These are illustrative entries, not verified sign-language instructions.
SIGNS = [
    {
        "id": 1,
        "word": "Hello",
        "category": "Greetings",
        "description": "A greeting used when meeting someone.",
        "image": "/static/signs/hello.png",
        "language": "ASL"
    },
    {
        "id": 2,
        "word": "Thank you",
        "category": "Greetings",
        "description": "Used to express gratitude.",
        "image": "/static/signs/thank-you.png",
        "language": "ASL"
    },
    {
        "id": 3,
        "word": "Please",
        "category": "Common phrases",
        "description": "Used to make a polite request.",
        "image": "/static/signs/please.png",
        "language": "ASL"
    },
    {
        "id": 4,
        "word": "Yes",
        "category": "Common words",
        "description": "An affirmative response.",
        "image": "/static/signs/yes.png",
        "language": "ASL"
    },
    {
        "id": 5,
        "word": "No",
        "category": "Common words",
        "description": "A negative response.",
        "image": "/static/signs/no.png",
        "language": "ASL"
    },
    {
        "id": 6,
        "word": "Help",
        "category": "Essential signs",
        "description": "Used to communicate a need for assistance.",
        "image": "/static/signs/help.png",
        "language": "ASL"
    },
    {
        "id": 7,
        "word": "Water",
        "category": "Everyday life",
        "description": "A sign associated with drinking water.",
        "image": "/static/signs/water.png",
        "language": "ASL"
    },
    {
        "id": 8,
        "word": "Sorry",
        "category": "Common phrases",
        "description": "Used to express an apology.",
        "image": "/static/signs/sorry.png",
        "language": "ASL"
    }
]


@dictionary_bp.route("/", methods=["GET"])
def get_dictionary():
    """Return all dictionary entries, with optional search filters."""
    query = request.args.get("q", "").strip().casefold()
    category = request.args.get("category", "").strip().casefold()
    language = request.args.get("language", "").strip().casefold()

    results = [
        sign for sign in SIGNS
        if query in sign["word"].casefold()
        or query in sign["description"].casefold()
        if not category or sign["category"].casefold() == category
        if not language or sign["language"].casefold() == language
    ]

    return jsonify({
        "status": "success",
        "count": len(results),
        "results": results
    })


@dictionary_bp.route("/<int:sign_id>", methods=["GET"])
def get_sign(sign_id):
    """Return one dictionary entry by ID."""
    sign = next(
        (item for item in SIGNS if item["id"] == sign_id),
        None
    )

    if sign is None:
        return jsonify({
            "status": "error",
            "message": "Sign not found"
        }), 404

    return jsonify({
        "status": "success",
        "result": sign
    })


@dictionary_bp.route("/categories", methods=["GET"])
def get_categories():
    """Return the available dictionary categories."""
    categories = sorted({sign["category"] for sign in SIGNS})

    return jsonify({
        "status": "success",
        "results": categories
    })
from dictionary import dictionary_bp

def create_app():
    app = Flask(__name__)

    CORS(app)

    app.register_blueprint(dictionary_bp)

    return app