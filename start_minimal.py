#!/usr/bin/env python3
"""
Script de démarrage minimal pour Railway
"""
import os
import sys
import subprocess
from pathlib import Path

def main():
    print("🚀 Démarrage minimal Railway...")
    
    # Configuration basique
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    # Variables d'environnement minimales
    if not os.environ.get('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'sqlite:///./najah_ai.db'
    
    if not os.environ.get('SECRET_KEY'):
        os.environ['SECRET_KEY'] = 'najah-ai-secret-key-2024'
    
    if not os.environ.get('JWT_SECRET_KEY'):
        os.environ['JWT_SECRET_KEY'] = 'najah-ai-jwt-secret-2024'
    
    print(f"🔧 Port: {port}")
    print(f"📁 DATABASE_URL: {os.environ.get('DATABASE_URL')}")
    
    try:
        # Changer vers le dossier backend
        backend_dir = Path(__file__).parent / "backend"
        os.chdir(backend_dir)
        sys.path.insert(0, str(backend_dir))
        
        print(f"📂 Répertoire de travail: {backend_dir}")
        
        # Importer et démarrer l'application
        from app import app
        print("✅ Application importée avec succès")
        
        import uvicorn
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

if __name__ == "__main__":
    main()
