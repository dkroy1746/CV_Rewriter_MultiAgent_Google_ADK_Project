"""Configuration module for CV Formatter."""
import os
from pathlib import Path
from dotenv import load_dotenv


class Config:
    """Application configuration."""

    def __init__(self):
        """Initialize configuration by loading environment variables."""
        # Load .env file from project root
        env_path = Path(__file__).parent.parent / ".env"
        load_dotenv(dotenv_path=env_path)

        # Get API key
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        if not self.google_api_key:
            raise ValueError(
                "GOOGLE_API_KEY not found in environment variables. "
                "Please create a .env file with GOOGLE_API_KEY=your_key"
            )

        # Set environment variable for Google SDK
        os.environ["GOOGLE_API_KEY"] = self.google_api_key

        # App configuration
        self.app_name = os.getenv("APP_NAME", "agents")
        self.user_id = os.getenv("USER_ID", "default_user")

        # Model configuration
        self.model_name = os.getenv("MODEL_NAME", "gemini-2.5-flash")

    @property
    def is_configured(self) -> bool:
        """Check if configuration is valid."""
        return bool(self.google_api_key)


# Global config instance
config = Config()
