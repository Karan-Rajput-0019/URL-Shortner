"""
WSGI entry point for production deployment.
"""
import os
from app import app
from config import config

# Get configuration from environment
config_name = os.getenv('FLASK_ENV', 'production')
app.config.from_object(config[config_name])

# Validate configuration
config[config_name].validate()

if __name__ == "__main__":
    app.run()

