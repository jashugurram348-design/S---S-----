
from flask import Flask, jsonify
from flask_cors import CORS


def create_app():
    app = Flask(__name__)

    # Enable frontend-to-backend requests
    CORS(app)

    # Register API blueprints
    from dictionary import dictionary_bp
    from history import history_bp
    from learn import learn_bp
    from sos import sos_bp
    from translate import translate_bp

    app.register_blueprint(dictionary_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(learn_bp)
    app.register_blueprint(sos_bp)
    app.register_blueprint(translate_bp)

    # Main API route
    @app.route("/", methods=["GET"])
    def home():
        return jsonify({
            "success": True,
            "app": "SignSpeak API",
            "message": "Backend is running"
        })

    # Health check route
    @app.route("/health", methods=["GET"])
    def health():
        return jsonify({
            "success": True,
            "status": "healthy"
        })

    # Handle unknown routes
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": "API endpoint not found"
        }), 404

    return app
