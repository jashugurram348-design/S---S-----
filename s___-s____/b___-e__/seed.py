
from __init__ import create_app
from database import db
from models import DictionaryEntry, Lesson


# Sample dictionary entries for development.
# Verify sign descriptions and demonstrations with an ISL expert
# before presenting them as authoritative sign-language content.
DICTIONARY_DATA = [
    {
        "word": "Hello",
        "description": "A greeting used when meeting someone.",
        "category": "Greetings",
        "language": "ISL",
    },
    {
        "word": "Thank you",
        "description": "A polite expression of gratitude.",
        "category": "Common phrases",
        "language": "ISL",
    },
    {
        "word": "Help",
        "description": "Used to communicate a need for assistance.",
        "category": "Essential words",
        "language": "ISL",
    },
    {
        "word": "Yes",
        "description": "Used to express agreement or affirmation.",
        "category": "Essential words",
        "language": "ISL",
    },
    {
        "word": "No",
        "description": "Used to express disagreement or negation.",
        "category": "Essential words",
        "language": "ISL",
    },
    {
        "word": "Sorry",
        "description": "Used to express an apology.",
        "category": "Common phrases",
        "language": "ISL",
    },
]

# Beginner learning lessons.
LESSON_DATA = [
    {
        "title": "Introduction to Sign Language",
        "description": (
            "Learn about sign languages, visual communication, "
            "and respectful communication with Deaf people."
        ),
        "category": "Basics",
        "difficulty": "Beginner",
        "duration_minutes": 5,
    },
    {
        "title": "Everyday Greetings",
        "description": (
            "Explore greetings and introductions using "
            "verified sign-language learning resources."
        ),
        "category": "Greetings",
        "difficulty": "Beginner",
        "duration_minutes": 10,
    },
    {
        "title": "Common Everyday Words",
        "description": (
            "Learn useful everyday vocabulary with verified "
            "sign demonstrations."
        ),
        "category": "Vocabulary",
        "difficulty": "Beginner",
        "duration_minutes": 10,
    },
    {
        "title": "Communicating Needs",
        "description": (
            "Practise communicating everyday needs and asking "
            "for assistance using verified learning materials."
        ),
        "category": "Communication",
        "difficulty": "Beginner",
        "duration_minutes": 10,
    },
]


def seed_dictionary():
    """Add dictionary entries that do not already exist."""
    added = 0

    for item in DICTIONARY_DATA:
        existing = DictionaryEntry.query.filter_by(
            word=item["word"],
            language=item["language"],
        ).first()

        if existing is None:
            db.session.add(DictionaryEntry(**item))
            added += 1

    return added


def seed_lessons():
    """Add lessons that do not already exist."""
    added = 0

    for item in LESSON_DATA:
        existing = Lesson.query.filter_by(
            title=item["title"]
        ).first()

        if existing is None:
            db.session.add(Lesson(**item))
            added += 1

    return added


def seed_database():
    """Initialize tables and insert sample data."""
    app = create_app()

    with app.app_context():
        # Import models before creating tables.
        db.create_all()

        dictionary_count = seed_dictionary()
        lesson_count = seed_lessons()

        try:
            db.session.commit()
            print("SignSpeak database seeded successfully.")
            print(f"Dictionary entries added: {dictionary_count}")
            print(f"Lessons added: {lesson_count}")

        except Exception as error:
            db.session.rollback()
            print(f"Database seeding failed: {error}")
            raise

        finally:
            db.session.remove()


if __name__ == "__main__":
    seed_database()

cd backend
python seed.py

