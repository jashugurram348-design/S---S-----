
"""
SignSpeak - Emergency Assistance API

Demo functionality for creating and viewing SOS requests.
This starter version does NOT send real emergency alerts.
"""

from datetime import datetime, timezone
from uuid import uuid4

from flask import Blueprint, jsonify, request

sos_bp = Blueprint("sos", __name__, url_prefix="/api/sos")

# Temporary in-memory storage. Data resets when the server restarts.
sos_requests = []

EMERGENCY_TYPES = {
    "medical",
    "safety",
    "communication",
    "other"
}

# These are general emergency numbers for India.
# Verify local availability before relying on them.
EMERGENCY_CONTACTS = [
    {
        "name": "National Emergency Response",
        "number": "112",
        "region": "India"
    },
    {
        "name": "Ambulance",
        "number": "108",
        "region": "India; availability may vary"
    }
]


@sos_bp.route("/contacts", methods=["GET"])
def get_emergency_contacts():
    """Return configured emergency contact information."""
    return jsonify({
        "status": "success",
        "results": EMERGENCY_CONTACTS
    })


@sos_bp.route("/request", methods=["POST"])
def create_sos_request():
    """Create an SOS request for the application to track."""
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "status": "error",
            "message": "A JSON request body is required."
        }), 400

    emergency_type = data.get("type", "other")
    message = data.get("message", "")

    if not isinstance(emergency_type, str):
        return jsonify({
            "status": "error",
            "message": "Emergency type must be a string."
        }), 400

    emergency_type = emergency_type.strip().lower()

    if emergency_type not in EMERGENCY_TYPES:
        return jsonify({
            "status": "error",
            "message": "Choose medical, safety, communication, or other."
        }), 400

    if not isinstance(message, str):
        return jsonify({
            "status": "error",
            "message": "Message must be a string."
        }), 400

    message = message.strip()

    if len(message) > 1000:
        return jsonify({
            "status": "error",
            "message": "Message must not exceed 1000 characters."
        }), 400

    record = {
        "id": str(uuid4()),
        "type": emergency_type,
        "message": message,
        "status": "received_by_demo_app",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    sos_requests.append(record)

    return jsonify({
        "status": "success",
        "message": (
            "Demo request recorded. No emergency services "
            "or contacts have been notified."
        ),
        "result": record
    }), 201


@sos_bp.route("/requests", methods=["GET"])
def get_sos_requests():
    """List SOS requests recorded by this demo application."""
    return jsonify({
        "status": "success",
        "count": len(sos_requests),
        "results": list(reversed(sos_requests))
    })


@sos_bp.route("/requests/<string:request_id>", methods=["GET"])
def get_sos_request(request_id):
    """Retrieve one SOS request by its ID."""
    record = next(
        (item for item in sos_requests if item["id"] == request_id),
        None
    )

    if record is None:
        return jsonify({
            "status": "error",
            "message": "SOS request not found."
        }), 404

    return jsonify({
        "status": "success",
        "result": record
    })
