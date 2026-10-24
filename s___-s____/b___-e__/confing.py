
import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from the backend directory
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


def env_bool(name, default=False):
    """Read a boolean environment variable."""
    value = os.getenv(name)

    if value is None:
        return default

    return value.strip().lower() in ("true", "1", "yes", "on")


def env_float(name, default, minimum=0.0, maximum=1.0):
    """Read and validate a float environment variable."""
    try:
        value = float(os.getenv(name, str(default)))
    except (TypeError, ValueError):
        value = default

    return max(minimum, min(value, maximum))


class Config:
    """Base configuration for SignSpeak."""

    # Flask
    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "development-only-change-this-key"
    )
    DEBUG = env_bool("DEBUG", False)
    PORT = int(os.getenv("PORT", "5000"))

    # Database
    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'signspeak.db'}"
    )
    SQLALCHEMY_DATABASE_URI = DATABASE_URL
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Frontend and CORS
    FRONTEND_URL = os.getenv(
        "FRONTEND_URL",
        "http://localhost:3000"
    )

    # Translation defaults
    DEFAULT_SOURCE_LANGUAGE = os.getenv(
        "DEFAULT_SOURCE_LANGUAGE", "en"
    )
    DEFAULT_TARGET_LANGUAGE = os.getenv(
        "DEFAULT_TARGET_LANGUAGE", "te"
    )

    # Speech
    DEFAULT_SPEECH_LANGUAGE = os.getenv(
        "DEFAULT_SPEECH_LANGUAGE", "en-IN"
    )

    try:
        SPEECH_RATE = int(os.getenv("SPEECH_RATE", "160"))
    except ValueError:
        SPEECH_RATE = 160

    # Hand detection
    try:
        MAX_HANDS = max(1, min(
            int(os.getenv("MAX_HANDS", "2")), 2
        ))
    except ValueError:
        MAX_HANDS = 2

    HAND_DETECTION_CONFIDENCE = env_float(
        "HAND_DETECTION_CONFIDENCE", 0.6
    )
    HAND_TRACKING_CONFIDENCE = env_float(
        "HAND_TRACKING_CONFIDENCE", 0.6
    )

    # Logging
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = False


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
