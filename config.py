import os
from typing import Optional

class Settings:
    # MongoDB settings
    MONGODB_URI: str = os.getenv("MONGODB_URI", "mongodb+srv://atharvaj:D13hJoR1fRkMMpO4@letsupgrade.vsucyfj.mongodb.net/video_tagging?retryWrites=true&w=majority")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME", "video_tagging")
    
    # File upload settings
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    ALLOWED_VIDEO_TYPES: list = [
        "video/mp4",
        "video/avi",
        "video/mov",
        "video/wmv",
        "video/flv",
        "video/webm",
        "video/mkv"
    ]
    
    # KeyBERT settings
    MAX_TAGS: int = 20
    
    # API settings
    API_TITLE: str = "Video Tagging API"
    API_VERSION: str = "1.0.0"
    
    # CORS settings
    CORS_ORIGINS: list = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Add your frontend URL for production
    if os.getenv("FRONTEND_URL"):
        CORS_ORIGINS.append(os.getenv("FRONTEND_URL"))

settings = Settings() 