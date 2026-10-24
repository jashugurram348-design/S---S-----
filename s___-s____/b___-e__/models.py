
from datetime import datetime, timezone
from database import db


def utc_now():
    """Return the current UTC time."""
    return datetime.now(timezone.utc)


class TranslationHistory(db.Model):
    __tablename__ = "translation_history"

    id = db.Column(db.Integer, primary_key=True)
    original_text = db.Column(db.Text, nullable=False)
    translated_text = db.Column(db.Text, nullable=False)
    source_language = db.Column(
        db.String(20), nullable=False, default="en"
    )
    target_language = db.Column(
        db.String(20), nullable=False, default="te"
    )
    mode = db.Column(db.String(20), nullable=False, default="text")
    created_at = db.Column(
        db.DateTime(timezone=True), default=utc_now, nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "original_text": self.original_text,
            "translated_text": self.translated_text,
            "source_language": self.source_language,
            "target_language": self.target_language,
            "mode": self.mode,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
        }


class DictionaryEntry(db.Model):
    __tablename__ = "dictionary_entries"

    id = db.Column(db.Integer, primary_key=True)
    word = db.Column(db.String(100), nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.String(50), nullable=False, default="General"
    )
    language = db.Column(
        db.String(20), nullable=False, default="ISL"
    )
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=utc_now, nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "word": self.word,
            "description": self.description,
            "category": self.category,
            "language": self.language,
            "image_url": self.image_url,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
        }


class Lesson(db.Model):
    __tablename__ = "lessons"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.String(50), nullable=False, default="Beginner"
    )
    difficulty = db.Column(
        db.String(30), nullable=False, default="Beginner"
    )
    duration_minutes = db.Column(
        db.Integer, nullable=False, default=5
    )
    image_url = db.Column(db.String(500), nullable=True)
    created_at = db.Column(
        db.DateTime(timezone=True), default=utc_now, nullable=False
    )

    progress = db.relationship(
        "LessonProgress",
        back_populates="lesson",
        cascade="all, delete-orphan",
    )

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "difficulty": self.difficulty,
            "duration_minutes": self.duration_minutes,
            "image_url": self.image_url,
        }


class LessonProgress(db.Model):
    __tablename__ = "lesson_progress"

    id = db.Column(db.Integer, primary_key=True)
    lesson_id = db.Column(
        db.Integer,
        db.ForeignKey("lessons.id"),
        nullable=False,
        index=True,
    )
    learner_id = db.Column(
        db.String(100), nullable=False, default="local-user"
    )
    completed = db.Column(db.Boolean, default=False, nullable=False)
    completed_at = db.Column(
        db.DateTime(timezone=True), nullable=True
    )

    lesson = db.relationship("Lesson", back_populates="progress")

    __table_args__ = (
        db.UniqueConstraint(
            "lesson_id",
            "learner_id",
            name="uq_lesson_learner",
        ),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "lesson_id": self.lesson_id,
            "learner_id": self.learner_id,
            "completed": self.completed,
            "completed_at": self.completed_at.isoformat()
            if self.completed_at else None,
        }


class SOSRequest(db.Model):
    __tablename__ = "sos_requests"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    message = db.Column(db.Text, nullable=False)
    status = db.Column(
        db.String(30), nullable=False, default="created"
    )
    created_at = db.Column(
        db.DateTime(timezone=True), default=utc_now, nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "message": self.message,
            "status": self.status,
            "created_at": self.created_at.isoformat()
            if self.created_at else None,
        }
