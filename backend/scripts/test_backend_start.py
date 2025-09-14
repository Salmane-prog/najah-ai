#!/usr/bin/env python3
"""
Script pour tester le démarrage du backend
"""

import subprocess
import time
import requests

def test_backend_start():
    print("🚀 Test du démarrage du backend...")
    
    try:
        # Démarrer le backend en arrière-plan
        process = subprocess.Popen(
            ["uvicorn", "app:app", "--reload", "--host", "0.0.0.0", "--port", "8000"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        
        print("⏳ Attente du démarrage...")
        time.sleep(5)  # Attendre 5 secondes
        
        # Tester si le serveur répond
        try:
            response = requests.get("http://localhost:8000/docs", timeout=5)
            if response.status_code == 200:
                print("✅ Backend démarré avec succès")
                print("📊 Test de l'endpoint dashboard-data...")
                
                # Test rapide de l'endpoint
                test_response = requests.get("http://localhost:8000/api/v1/dashboard/dashboard-data")
                print(f"   Status: {test_response.status_code}")
                
            else:
                print(f"❌ Backend répond mais avec status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print("❌ Backend ne répond pas")
        except Exception as e:
            print(f"❌ Erreur lors du test: {e}")
        
        # Arrêter le processus
        process.terminate()
        process.wait()
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")

if __name__ == "__main__":
    test_backend_start() 