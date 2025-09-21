#!/usr/bin/env python3
"""
Script de démarrage pour Railway
Initialise la base de données et démarre le serveur
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 DÉMARRAGE SUR RAILWAY")
    print("=" * 40)
    
    # Vérifier les variables d'environnement
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        print(f"✅ DATABASE_URL configurée")
        # Convertir PostgreSQL URL en SQLAlchemy format
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
            os.environ["DATABASE_URL"] = database_url
    else:
        print("⚠️ DATABASE_URL non configurée, utilisation de SQLite")
        os.environ["DATABASE_URL"] = "sqlite:///./najah_ai.db"
    
    # Créer les tables si nécessaire
    try:
        from database import engine
        from models import Base
        print("📊 Création des tables...")
        Base.metadata.create_all(bind=engine)
        print("✅ Tables créées avec succès")
    except Exception as e:
        print(f"⚠️ Erreur lors de la création des tables: {e}")
    
    # Importer les données initiales si nécessaire
    try:
        from init_production_data import main as init_data
        print("📋 Initialisation des données...")
        init_data()
        print("✅ Données initialisées")
    except Exception as e:
        print(f"⚠️ Erreur lors de l'initialisation des données: {e}")
    
    # Démarrer le serveur
    print("🌐 Démarrage du serveur FastAPI...")
    os.system("uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1")

if __name__ == "__main__":
    main()