#!/usr/bin/env python3
"""
Script pour démarrer le serveur backend
"""

import subprocess
import time
import requests
import sys
import os

def check_backend_running():
    """Vérifier si le backend est déjà en cours d'exécution"""
    try:
        response = requests.get("http://localhost:8000/", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_backend():
    """Démarrer le serveur backend"""
    print("🚀 Démarrage du serveur backend...")
    
    # Vérifier si le backend est déjà en cours d'exécution
    if check_backend_running():
        print("✅ Le serveur backend est déjà en cours d'exécution sur le port 8000")
        return True
    
    # Vérifier que nous sommes dans le bon répertoire
    if not os.path.exists("backend/app.py"):
        print("❌ Erreur: Le fichier backend/app.py n'existe pas")
        print("💡 Assurez-vous d'être dans le répertoire racine du projet")
        return False
    
    try:
        # Démarrer le serveur
        print("📁 Changement vers le répertoire backend...")
        os.chdir("backend")
        
        print("🔧 Démarrage du serveur avec uvicorn...")
        process = subprocess.Popen([
            sys.executable, "-m", "uvicorn", "app:fastapi_app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        # Attendre un peu que le serveur démarre
        print("⏳ Attente du démarrage du serveur...")
        time.sleep(5)
        
        # Vérifier si le serveur est maintenant accessible
        if check_backend_running():
            print("✅ Serveur backend démarré avec succès sur http://localhost:8000")
            print("📚 Documentation disponible sur http://localhost:8000/docs")
            return True
        else:
            print("❌ Le serveur n'a pas pu démarrer correctement")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return False

if __name__ == "__main__":
    if start_backend():
        print("\n🎉 Le serveur backend est prêt !")
        print("💡 Vous pouvez maintenant tester les endpoints du professeur")
    else:
        print("\n💥 Échec du démarrage du serveur backend")
        print("💡 Vérifiez les logs pour plus de détails")









