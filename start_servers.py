#!/usr/bin/env python3
"""
Script de démarrage automatique des serveurs Najah AI
"""

import subprocess
import time
import sys
import os
from pathlib import Path

def start_backend():
    """Démarrer le serveur backend"""
    print("🚀 Démarrage du serveur backend...")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Dossier backend non trouvé")
        return False
    
    try:
        # Démarrer le serveur backend
        backend_process = subprocess.Popen(
            [sys.executable, "-m", "uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            cwd=backend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Attendre que le serveur démarre
        time.sleep(5)
        
        if backend_process.poll() is None:
            print("✅ Serveur backend démarré avec succès")
            return backend_process
        else:
            print("❌ Échec du démarrage du serveur backend")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du backend: {e}")
        return False

def start_frontend():
    """Démarrer le serveur frontend"""
    print("🎨 Démarrage du serveur frontend...")
    
    frontend_dir = Path("frontend")
    if not frontend_dir.exists():
        print("❌ Dossier frontend non trouvé")
        return False
    
    try:
        # Démarrer le serveur frontend
        frontend_process = subprocess.Popen(
            ["npm", "run", "dev"],
            cwd=frontend_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        # Attendre que le serveur démarre
        time.sleep(10)
        
        if frontend_process.poll() is None:
            print("✅ Serveur frontend démarré avec succès")
            return frontend_process
        else:
            print("❌ Échec du démarrage du serveur frontend")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du frontend: {e}")
        return False

def check_servers():
    """Vérifier que les serveurs sont accessibles"""
    import requests
    
    print("🔍 Vérification des serveurs...")
    
    # Test backend
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        if response.status_code == 200:
            print("✅ Backend accessible")
            backend_ok = True
        else:
            print(f"❌ Backend inaccessible: {response.status_code}")
            backend_ok = False
    except:
        print("❌ Backend non accessible")
        backend_ok = False
    
    # Test frontend
    try:
        response = requests.get("http://localhost:3001/", timeout=5)
        if response.status_code == 200:
            print("✅ Frontend accessible")
            frontend_ok = True
        else:
            print(f"❌ Frontend inaccessible: {response.status_code}")
            frontend_ok = False
    except:
        print("❌ Frontend non accessible")
        frontend_ok = False
    
    return backend_ok and frontend_ok

def main():
    """Fonction principale"""
    print("🚀 Démarrage automatique des serveurs Najah AI")
    print("="*50)
    
    # Démarrer le backend
    backend_process = start_backend()
    if not backend_process:
        print("❌ Impossible de démarrer le backend")
        return
    
    # Démarrer le frontend
    frontend_process = start_frontend()
    if not frontend_process:
        print("❌ Impossible de démarrer le frontend")
        backend_process.terminate()
        return
    
    # Vérifier que les serveurs sont accessibles
    time.sleep(5)
    if check_servers():
        print("\n🎉 Tous les serveurs sont opérationnels!")
        print("📱 Frontend: http://localhost:3001")
        print("🌐 Backend: http://localhost:8000")
        print("📚 API Docs: http://localhost:8000/docs")
        
        try:
            print("\n⏳ Appuyez sur Ctrl+C pour arrêter les serveurs...")
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n🛑 Arrêt des serveurs...")
            backend_process.terminate()
            frontend_process.terminate()
            print("✅ Serveurs arrêtés")
    else:
        print("❌ Problème avec les serveurs")
        backend_process.terminate()
        frontend_process.terminate()

if __name__ == "__main__":
    main() 