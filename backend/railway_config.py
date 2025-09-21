"""
Configuration spécifique pour Railway
"""
import os
from pathlib import Path

def setup_railway_environment():
    """Configure l'environnement pour Railway"""
    
    # Forcer les variables d'environnement nécessaires
    if not os.environ.get('DATABASE_URL'):
        # Utiliser SQLite en production
        db_path = Path(__file__).parent / "najah_ai.db"
        os.environ['DATABASE_URL'] = f"sqlite:///{db_path}"
        print(f"📁 Base de données SQLite configurée: {db_path}")
    
    # Variables de sécurité par défaut
    if not os.environ.get('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'najah-ai-secret-key-super-secure-2024'
    
    if not os.environ.get('JWT_SECRET_KEY'):
        os.environ['JWT_SECRET_KEY'] = 'najah-ai-jwt-secret-key-ultra-secure-2024'
    
    # CORS pour production
    if not os.environ.get('CORS_ORIGINS'):
        os.environ['CORS_ORIGINS'] = '*'
    
    print("✅ Configuration Railway appliquée")

# Appeler automatiquement la configuration
setup_railway_environment()
