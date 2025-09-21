#!/usr/bin/env python3
"""
Script de démarrage ULTRA-minimal pour Railway
"""
import os
import sys
from pathlib import Path

print("🚀 Démarrage ULTRA-minimal Railway...")
print(f"🐍 Python version: {sys.version}")

# Configuration basique
port = int(os.environ.get("PORT", 8000))
host = "0.0.0.0"

# Variables d'environnement minimales
os.environ['DATABASE_URL'] = os.environ.get('DATABASE_URL', 'sqlite:///./najah_ai.db')
os.environ['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'najah-ai-secret-key-2024')
os.environ['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY', 'najah-ai-jwt-secret-2024')

print(f"🔧 Port: {port}")
print(f"📁 DATABASE_URL: {os.environ.get('DATABASE_URL')}")

try:
    # Changer vers le dossier backend
    backend_dir = Path(__file__).parent / "backend"
    os.chdir(backend_dir)
    sys.path.insert(0, str(backend_dir))
    
    print(f"📂 Répertoire de travail: {backend_dir}")
    
    # Test d'import minimal
    print("🔍 Test d'import des modules...")
    
    try:
        import fastapi
        print("✅ FastAPI importé")
    except ImportError as e:
        print(f"❌ FastAPI: {e}")
    
    try:
        import pydantic
        print("✅ Pydantic importé")
    except ImportError as e:
        print(f"❌ Pydantic: {e}")
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy importé")
    except ImportError as e:
        print(f"❌ SQLAlchemy: {e}")
    
    try:
        import jwt
        print("✅ PyJWT importé")
    except ImportError as e:
        print(f"❌ PyJWT: {e}")
    
    try:
        from jose import jwt as jose_jwt
        print("✅ python-jose JWT importé")
    except ImportError as e:
        print(f"❌ python-jose JWT: {e}")
    
    # Importer et démarrer l'application
    print("🚀 Import de l'application...")
    from app import app
    print("✅ Application importée avec succès")
    
    import uvicorn
    print(f"🌐 Démarrage du serveur sur {host}:{port}")
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info",
        access_log=True
    )
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
