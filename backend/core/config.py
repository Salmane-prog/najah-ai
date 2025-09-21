import os
from dotenv import load_dotenv

load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../.env'))

class Settings:
    PROJECT_NAME: str = "Plateforme éducative IA"
    PROJECT_VERSION: str = "1.0"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "supersecret")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    ALGORITHM: str = os.getenv("ALGORITHM", "HS256")
    
    # Configuration de base de données dynamique
    SQLALCHEMY_DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./najah_ai.db")
    
    BACKEND_CORS_ORIGINS: list = os.getenv("BACKEND_CORS_ORIGINS", "*").split(",")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
settings = Settings() 