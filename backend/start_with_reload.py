#!/usr/bin/env python3
"""
Script pour démarrer le serveur avec reload fonctionnel
"""

import subprocess
import sys
import os

def start_with_reload():
    print("=== DÉMARRAGE AVEC RELOAD FONCTIONNEL ===")
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("app.py"):
        print("❌ Erreur: app.py non trouvé. Assurez-vous d'être dans le répertoire backend")
        return
    
    print("✅ Fichier app.py trouvé")
    print("🚀 Démarrage avec uvicorn et reload...")
    print("   URL: http://localhost:8000")
    print("   Health check: http://localhost:8000/health")
    print("   Appuyez sur Ctrl+C pour arrêter")
    
    try:
        # Démarrer uvicorn avec reload
        subprocess.run([
            sys.executable, "-m", "uvicorn",
            "app:app",
            "--reload",
            "--port", "8000",
            "--host", "127.0.0.1"
        ])
    except KeyboardInterrupt:
        print("\n✅ Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")

if __name__ == "__main__":
    start_with_reload() 