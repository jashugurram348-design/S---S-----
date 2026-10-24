
"""
SignSpeak - Learning Module API
Provides lessons and learning progress endpoints.
"""

from flask import Blueprint, jsonify, request

learn_bp = Blueprint("learn", __name__, url_prefix="/api/learn")


# Starter lessons. Add verified ASL or ISL content as needed.
LESSONS = [
    {
        "id": 1,
        "title": "Basic Greetings",
        "category": "Beginner",
        "description": "Learn common greeting signs.",
        "signs": ["Hello", "Good morning", "Goodbye"],
        "duration_minutes": 10
    },
    {
        "id": 2,
        "title": "Everyday Words",
        "category": "Beginner",
        "description": "Practice useful everyday vocabulary.",
        "signs": ["Water", "Food", "Home"],
        "duration_minutes": 15
    },
    {
        "id": 3,
        "title": "Common Phrases",
        "category": "Beginner",
        "description": "Explore polite and helpful phrases.",
        "signs": ["Please", "Thank you", "Sorry", "Help"],
        "duration_minutes": 15
    },
    {
        "id": 4,
        "title": "Numbers",
        "category": "Practice",
        "description": "Start learning number signs.",
        "signs": ["One", "Two", "Three", "Four", "Five"],
        "duration_minutes": 12
    }
]

# Temporary in-memory progress; resets when the server restarts.
completed_lessons = set()


@learn_bp.route("/lessons", methods=["GET"])
def get_lessons():
    """Return all lessons and completion status."""
    results = []

    for lesson in LESSONS:
        item = lesson.copy()
        item["completed"] = item["id"] in completed_lessons
        results.append(item)

    return jsonify({
        "status": "success",
        "count": len(results),
        "results": results
    })


@learn_bp.route("/lessons/<int:lesson_id>", methods=["GET"])
def get_lesson(lesson_id):
    """Return one lesson."""
    lesson = next(
        (item for item in LESSONS if item["id"] == lesson_id),
        None
    )

    if lesson is None:
        return jsonify({
            "status": "error",
            "message": "Lesson not found."
        }), 404

    result = lesson.copy()
    result["completed"] = lesson_id in completed_lessons

    return jsonify({
        "status": "success",
        "result": result
    })


@learn_bp.route("/lessons/<int:lesson_id>/complete", methods=["POST"])
def complete_lesson(lesson_id):
    """Mark a lesson as completed."""
    if not any(lesson["id"] == lesson_id for lesson in LESSONS):
        return jsonify({
            "status": "error",
            "message": "Lesson not found."
        }), 404

    completed_lessons.add(lesson_id)

    return jsonify({
        "status": "success",
        "message": "Lesson completed!",
        "lesson_id": lesson_id,
        "progress": get_progress_data()
    })


@learn_bp.route("/progress", methods=["GET"])
def get_progress():
    """Return overall learning progress."""
    return jsonify({
        "status": "success",
        "result": get_progress_data()
    })


def get_progress_data():
    total = len(LESSONS)
    completed = len(completed_lessons)

    return {
        "completed_lessons": completed,
        "total_lessons": total,
        "percentage": round(completed / total * 100) if total else 0
    }
