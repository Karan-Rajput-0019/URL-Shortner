import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY', 'dev-secret-key-change-in-production')
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    
    # Rate limiting
    RATELIMIT_STORAGE_URL = os.getenv('REDIS_URL', 'memory://')
    
    # QR Code settings
    QR_CODE_SIZE = 10
    QR_CODE_BORDER = 5
    
    # URL settings
    SHORT_ID_LENGTH = 6
    MAX_URL_LENGTH = 2048
    
    @staticmethod
    def validate():
        """Validate required configuration."""
        if not Config.SUPABASE_URL:
            raise ValueError("SUPABASE_URL environment variable is required")
        if not Config.SUPABASE_KEY:
            raise ValueError("SUPABASE_KEY environment variable is required")

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    ENV = 'development'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    ENV = 'production'
    
    # Override with more secure settings for production
    SECRET_KEY = os.getenv('FLASK_SECRET_KEY')
    
    @staticmethod
    def validate():
        """Additional validation for production."""
        Config.validate()
        if not ProductionConfig.SECRET_KEY or ProductionConfig.SECRET_KEY == 'dev-secret-key-change-in-production':
            raise ValueError("FLASK_SECRET_KEY must be set to a secure value in production")

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

