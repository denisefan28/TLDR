import os

# Base directory of the project
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Configuration settings
class Config:
    # Secret key for session management and security
    SECRET_KEY = 'your-secret-key-here'  # Replace with a strong secret key

    # File upload configuration
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    SUMMARY_FOLDER = os.path.join(BASE_DIR, 'summaries')
    ALLOWED_EXTENSIONS = {'mp4', 'txt'}

    # Ensure upload and summary folders exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    os.makedirs(SUMMARY_FOLDER, exist_ok=True)

    # NLP model configuration (optional)
    NLP_MODEL_NAME = 'facebook/bart-large-cnn'  # Default NLP model for summarization

    # Video processing configuration (optional)
    VIDEO_CODEC = 'libx264'
    VIDEO_RESOLUTION = (1280, 720)  # Width x Height

    # Debug mode (set to False in production)
    DEBUG = True  # Set to False in production

# Environment-specific configurations
class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

# Configuration mapping
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}