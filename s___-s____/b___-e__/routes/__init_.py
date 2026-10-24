from history import history_bp

# Inside create_app(), before return app:
app.register_blueprint(history_bp)

from flask import Flask
from flask_cors import CORS

def create_app():
    """Create and configure the SignSpeak Flask application."""

    app = Flask(__name__)

    # Basic application configuration
    app.config["SECRET_KEY"] = "change-this-before-deployment"
    app.config["JSON_SORT_KEYS"] = False

    # Enable CORS for frontend API requests.
    # Restrict origins to your frontend URL in production.
    CORS(app)

    @app.route("/")
    def home():
        return {
            "app": "SignSpeak",
            "message": "SignSpeak API is running!",
            "status": "success"
        }

    @app.route("/api/health")
    def health():
        return {
            "status": "healthy",
            "service": "SignSpeak API"
        }

    return app
from __init__ import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, port=5000)