
import os
from dotenv import load_dotenv
from __init__ import create_app

# Load environment variables from backend/.env
load_dotenv()

# Create the Flask application
app = create_app()


@app.route("/api/status", methods=["GET"])
def api_status():
    return {
        "success": True,
        "app": "SignSpeak",
        "status": "running",
        "version": "1.0.0"
    }, 200


if __name__ == "__main__":
    port = int(os.getenv("PORT", "5000"))
    debug = os.getenv("DEBUG", "False").lower() == "true"

    # Keep the development server local by default
    app.run(
        host="127.0.0.1",
        port=port,
        debug=debug
    )
