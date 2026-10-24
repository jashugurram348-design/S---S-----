
import os
from pathlib import Path

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import inspect, text
from sqlalchemy.exc import SQLAlchemyError

db = SQLAlchemy()


def init_db(app):
    """Configure the database and connect it to Flask."""
    base_dir = Path(__file__).resolve().parent

    database_url = app.config.get("SQLALCHEMY_DATABASE_URI") or os.getenv(
        "DATABASE_URL",
        f"sqlite:///{base_dir / 'signspeak.db'}"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = database_url
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    if database_url.startswith("sqlite"):
        app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {
            "connect_args": {"check_same_thread": False}
        }

    db.init_app(app)


def create_tables(app):
    """Create all database tables declared in models.py."""
    with app.app_context():
        import models  # Register database models
        db.create_all()
        print("Database and tables created successfully!")


def check_db_connection(app):
    """Check whether the database connection works."""
    with app.app_context():
        try:
            with db.engine.connect() as connection:
                connection.execute(text("SELECT 1"))

            return {
                "success": True,
                "message": "Database connection successful."
            }

        except SQLAlchemyError:
            app.logger.exception("Database connection failed")
            return {
                "success": False,
                "message": "Database connection failed."
            }


def get_table_names(app):
    """Return the names of tables in the database."""
    with app.app_context():
        return inspect(db.engine).get_table_names()


def reset_database(app):
    """Delete all existing tables and recreate them."""
    with app.app_context():
        import models  # Register database models
        db.drop_all()
        db.create_all()

        print("Database reset successfully.")
