
"""
SignSpeak - Translation History API
Save, retrieve, and delete translation history.
"""

from datetime import datetime, timezone

from flask import Blueprint, jsonify, request

history_bp = Blueprint(
    "history",
    __name__,
    url_prefix="/api/history"
)

# Temporary in-memory storage.
# Records are cleared when the server restarts.
history_records = []
next_history_id = 1


@history_bp.route("/", methods=["GET"])
def get_history():
    """Return translation history, newest first."""
    limit = request.args.get("limit", default=50, type=int)
    limit = max(1, min(limit or 50, 100))

    records = sorted(
        history_records,
        key=lambda item: item["created_at"],
        reverse=True
    )

    return jsonify({
        "status": "success",
        "count": len(records[:limit]),
        "results": records[:limit]
    })


@history_bp.route("/", methods=["POST"])
def add_history():
    """Save a translation to history."""
    global next_history_id

    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "A JSON request body is required."
        }), 400

    original_text = data.get("original_text", "")
    translated_text = data.get("translated_text", "")
    mode = data.get("mode", "text-to-sign")

    if not isinstance(original_text, str) or not isinstance(
        translated_text, str
    ):
        return jsonify({
            "status": "error",
            "message": "Translation fields must be strings."
        }), 400

    original_text = original_text.strip()
    translated_text = translated_text.strip()

    if not original_text or not translated_text:
        return jsonify({
            "status": "error",
            "message": "Both original_text and translated_text are required."
        }), 400

    if len(original_text) > 5000 or len(translated_text) > 5000:
        return jsonify({
            "status": "error",
            "message": "Text must not exceed 5000 characters."
        }), 400

    if mode not in ("text-to-sign", "sign-to-text"):
        return jsonify({
            "status": "error",
            "message": "Unsupported translation mode."
        }), 400

    record = {
        "id": next_history_id,
        "original_text": original_text,
        "translated_text": translated_text,
        "mode": mode,
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    history_records.append(record)
    next_history_id += 1

    return jsonify({
        "status": "success",
        "message": "Translation saved to history.",
        "result": record
    }), 201


@history_bp.route("/<int:history_id>", methods=["DELETE"])
def delete_history(history_id):
    """Delete one history record by ID."""
    for index, record in enumerate(history_records):
        if record["id"] == history_id:
            deleted_record = history_records.pop(index)

            return jsonify({
                "status": "success",
                "message": "History record deleted.",
                "result": deleted_record
            })

    return jsonify({
        "status": "error",
        "message": "History record not found."
    }), 404


@history_bp.route("/clear", methods=["DELETE"])
def clear_history():
    """Clear all history records."""
    history_records.clear()

    return jsonify({
        "status": "success",
        "message": "Translation history cleared."
    })
