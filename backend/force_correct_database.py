#!/usr/bin/env python3
"""
Script pour forcer l'utilisation de la bonne base de données
"""

import os
import sys

# Forcer l'utilisation de la bonne base de données
os.environ["SQLALCHEMY_DATABASE_URL"] = "sqlite:///F:/IMT/stage/Yancode/Najah__AI/data/app.db"

print("🔧 Configuration de la base de données...")
print(f"[DATABASE] Chemin forcé: {os.environ['SQLALCHEMY_DATABASE_URL']}")

# Ajouter le répertoire backend au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def test_database_connection():
    """Test de connexion à la base de données"""
    
    try:
        from core.database import engine
        from models.user import User
        from sqlalchemy import text
        
        print("✅ Connexion à la base de données réussie")
        
        # Test d'une requête simple
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM users"))
            count = result.scalar()
            print(f"✅ Nombre d'utilisateurs dans la base: {count}")
            
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

if __name__ == "__main__":
    test_database_connection() 