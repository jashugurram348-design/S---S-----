
import re
from flask import jsonify


def clean_text(value):
    """Remove extra whitespace from text input."""
    if not isinstance(value, str):
        return ""

    return " ".join(value.strip().split())


def validate_required_fields(data, required_fields):
    """
    Check that required fields exist and are not empty.

    Returns:
        (is_valid, missing_fields)
    """
    if not isinstance(data, dict):
        return False, list(required_fields)

    missing_fields = []

    for field in required_fields:
        value = data.get(field)

        if value is None:
            missing_fields.append(field)
        elif isinstance(value, str) and not value.strip():
            missing_fields.append(field)

    return len(missing_fields) == 0, missing_fields


def success_response(data=None, message="Success", status_code=200):
    """Create a consistent successful JSON response."""
    response = {
        "success": True,
        "message": message,
    }

    if data is not None:
        response["data"] = data

    return jsonify(response), status_code


def error_response(message="An error occurred", status_code=400):
    """Create a consistent error JSON response."""
    return jsonify({
        "success": False,
        "error": message,
    }), status_code


def paginate_items(items, page=1, per_page=10):
    """Return one page of items and pagination metadata."""
    try:
        page = int(page)
        per_page = int(per_page)
    except (TypeError, ValueError):
        raise ValueError("page and per_page must be integers")

    if page < 1:
        raise ValueError("page must be at least 1")

    if per_page < 1 or per_page > 100:
        raise ValueError("per_page must be between 1 and 100")

    total_items = len(items)
    start = (page - 1) * per_page
    end = start + per_page

    return {
        "items": items[start:end],
        "pagination": {
            "page": page,
            "per_page": per_page,
            "total_items": total_items,
            "total_pages": (
                (total_items + per_page - 1) // per_page
            ),
        },
    }


def is_valid_language_code(code):
    """Validate a basic language code such as en, en-IN, or te."""
    if not isinstance(code, str):
        return False

    return bool(re.fullmatch(
        r"[a-zA-Z]{2,3}(?:-[a-zA-Z]{2,4})?",
        code.strip()
    ))


def normalize_search_query(query):
    """Normalize a search query for case-insensitive matching."""
    return clean_text(query).casefold()


if __name__ == "__main__":
    sample = ["Hello", "Thank you", "Good morning"]

    print("Cleaned text:", clean_text("  Hello   world  "))
    print("Required fields:", validate_required_fields(
        {"text": "Hello"}, ["text", "mode"]
    ))
    print("Pagination:", paginate_items(sample, page=1, per_page=2))
    print("Language code valid:", is_valid_language_code("en-IN"))
