import os

from dotenv import load_dotenv


base_dir = os.path.abspath(os.path.dirname(__file__))

# Load environment variables from a local .env file in development.
# In production, the hosting provider's environment variables will take precedence.
env_path = os.path.join(base_dir, ".env")
if os.path.exists(env_path):
    load_dotenv(env_path, override=False)


class Config:
    """Central configuration for Flask app and database."""

    FLASK_ENV = os.getenv("FLASK_ENV", "development")

    # Debug is on by default in development, off otherwise (can be overridden explicitly).
    _default_debug = "1" if FLASK_ENV == "development" else "0"
    DEBUG = os.getenv("FLASK_DEBUG", _default_debug).lower() in ("1", "true", "yes", "on")

    # Default port for local development; most PaaS providers will inject PORT.
    PORT = int(os.getenv("PORT", "5000"))

    # Database configuration: fall back to the current class MySQL defaults if not provided.
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = int(os.getenv("DB_PORT", "3306"))
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")
    