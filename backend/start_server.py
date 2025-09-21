#!/usr/bin/env python3
"""
Script de démarrage robuste pour Railway
"""
import os
import sys
import uvicorn
from pathlib import Path

def main():
    # Ajouter le répertoire backend au path Python
    backend_dir = Path(__file__).parent
    sys.path.insert(0, str(backend_dir))
    
    # Configuration des variables d'environnement
    port = int(os.environ.get("PORT", 8000))
    host = "0.0.0.0"
    
    print(f"🚀 Démarrage du serveur sur {host}:{port}")
    print(f"📁 Répertoire de travail: {backend_dir}")
    print(f"🔧 Variables d'environnement:")
    print(f"   - PORT: {port}")
    print(f"   - PYTHON_ENV: {os.environ.get('PYTHON_ENV', 'development')}")
    print(f"   - DATABASE_URL: {'✅ Configurée' if os.environ.get('DATABASE_URL') else '❌ Non configurée'}")
    
    # Forcer les variables d'environnement pour la production
    if not os.environ.get('DATABASE_URL'):
        # Utiliser SQLite en production si pas de PostgreSQL
        db_path = backend_dir / "najah_ai.db"
        os.environ['DATABASE_URL'] = f"sqlite:///{db_path}"
        print(f"📁 Base de données SQLite: {db_path}")
    
    try:
        # Importer l'application
        from app import app
        print("✅ Application importée avec succès")
        
        # Démarrer le serveur
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True,
            reload=False
        )
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Erreur de démarrage: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()