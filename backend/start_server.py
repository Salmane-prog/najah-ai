#!/usr/bin/env python3
"""
Script de démarrage du serveur Najah AI Analytics
"""

import subprocess
import sys
import os
from pathlib import Path

def install_requirements():
    """Installer les dépendances Python"""
    print("📦 Installation des dépendances...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dépendances installées avec succès")
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors de l'installation des dépendances: {e}")
        return False
    return True

def start_server():
    """Démarrer le serveur FastAPI"""
    print("🚀 Démarrage du serveur Najah AI Analytics...")
    try:
        # Démarrer le serveur avec uvicorn
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", "8000", 
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n⏹️ Serveur arrêté par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")

def main():
    """Fonction principale"""
    print("=" * 60)
    print("🚀 NAJAH AI ANALYTICS BACKEND")
    print("=" * 60)
    
    # Vérifier que nous sommes dans le bon répertoire
    if not Path("main.py").exists():
        print("❌ Erreur: main.py non trouvé. Assurez-vous d'être dans le répertoire backend/")
        return
    
    # Installer les dépendances
    if not install_requirements():
        return
    
    print("\n" + "=" * 60)
    print("🎯 SERVEUR PRÊT À DÉMARRER")
    print("=" * 60)
    print("📊 Endpoints disponibles:")
    print("   - Analytics: http://localhost:8000/api/v1/analytics/*")
    print("   - Test Tracking: http://localhost:8000/api/v1/test-tracking/*")
    print("   - Santé: http://localhost:8000/health")
    print("   - Documentation: http://localhost:8000/docs")
    print("   - Interface Swagger: http://localhost:8000/docs")
    print("   - Interface ReDoc: http://localhost:8000/redoc")
    print("\n🔑 Token d'authentification: najah_token")
    print("🌐 CORS activé pour localhost:3000 et localhost:3001")
    print("\n💡 Appuyez sur Ctrl+C pour arrêter le serveur")
    print("=" * 60)
    
    # Démarrer le serveur
    start_server()

if __name__ == "__main__":
    main() 