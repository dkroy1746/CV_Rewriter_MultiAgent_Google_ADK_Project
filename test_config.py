"""Test configuration loading."""
from cv_formatter.config import config

print("Configuration Test")
print("=" * 50)
print(f"API Key Configured: {'✓' if config.is_configured else '✗'}")
print(f"Model Name: {config.model_name}")
print(f"App Name: {config.app_name}")
print(f"User ID: {config.user_id}")
print("=" * 50)
print("\n✓ Configuration loaded successfully!")
