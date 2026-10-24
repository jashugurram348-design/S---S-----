
import os

from dotenv import load_dotenv
from __init__ import create_app

# Load environment variables from .env
load_dotenv()

# Create the Flask application
app = create_app()


if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("DEBUG", "True").lower() == "true"

    app.run(
        host="127.0.0.1",
        port=port,
        debug=debug
    )
