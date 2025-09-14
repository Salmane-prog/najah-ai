from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import settings


engine = create_engine(settings.SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in settings.SQLALCHEMY_DATABASE_URL else {})
# Log du chemin réel utilisé par SQLite (utile pour debug)
if "sqlite" in str(engine.url):
    import os
    abs_path = os.path.abspath(engine.url.database)
    print(f"[DATABASE] Chemin base utilisée (absolu): {abs_path}")
print(f"[DATABASE] Chemin base utilisée: {settings.SQLALCHEMY_DATABASE_URL}")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Fonction pour obtenir la session de base de données
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Les imports explicites de modèles sont retirés pour éviter les circular imports.
# L'autocreate des tables peut être géré ailleurs si besoin.
# Base.metadata.create_all(bind=engine) 