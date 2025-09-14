#!/usr/bin/env python3
"""
Script pour diagnostiquer et corriger l'erreur 405 lors de la création de notes
"""

import requests
import json
import time
import subprocess
import sys
import os

def check_server_running():
    """Vérifier si le serveur backend est en cours d'exécution"""
    try:
        response = requests.get("http://localhost:8000/", timeout=5)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Démarrer le serveur backend"""
    print("🔄 Démarrage du serveur backend...")
    
    # Vérifier si le serveur est déjà en cours d'exécution
    if check_server_running():
        print("✅ Le serveur backend est déjà en cours d'exécution")
        return True
    
    try:
        # Démarrer le serveur en arrière-plan
        subprocess.Popen([
            sys.executable, "-c", 
            "import uvicorn; uvicorn.run('app:app', host='0.0.0.0', port=8000, reload=True)"
        ], cwd=os.getcwd())
        
        # Attendre que le serveur démarre
        print("⏳ Attente du démarrage du serveur...")
        for i in range(30):  # Attendre jusqu'à 30 secondes
            time.sleep(1)
            if check_server_running():
                print("✅ Serveur backend démarré avec succès!")
                return True
            print(f"⏳ Tentative {i+1}/30...")
        
        print("❌ Impossible de démarrer le serveur backend")
        return False
        
    except Exception as e:
        print(f"❌ Erreur lors du démarrage du serveur: {e}")
        return False

def test_notes_endpoint():
    """Tester l'endpoint de création de notes"""
    print("\n🧪 Test de l'endpoint de création de notes...")
    
    url = "http://localhost:8000/notes-advanced/"
    data = {
        "title": "Test de diagnostic",
        "content": "Ceci est un test pour diagnostiquer l'erreur 405",
        "subject": "Mathématiques",
        "chapter": "Test chapitre",
        "tags": "[\"test\", \"diagnostic\"]",
        "color": "bg-blue-100"
    }
    
    try:
        print(f"📡 Envoi de la requête POST à: {url}")
        print(f"📦 Données: {json.dumps(data, indent=2)}")
        
        response = requests.post(url, json=data, timeout=10)
        
        print(f"📊 Status: {response.status_code}")
        print(f"📋 Headers: {dict(response.headers)}")
        print(f"📄 Réponse: {response.text}")
        
        if response.status_code == 200:
            print("✅ Test réussi! L'endpoint fonctionne correctement")
            return True
        else:
            print(f"❌ Test échoué avec le status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def test_cors():
    """Tester les requêtes CORS"""
    print("\n🌐 Test des requêtes CORS...")
    
    url = "http://localhost:8000/notes-advanced/"
    headers = {
        'Content-Type': 'application/json',
        'Origin': 'http://localhost:3001',
        'Referer': 'http://localhost:3001/dashboard/student/notes-advanced'
    }
    
    try:
        # Test OPTIONS (preflight)
        print("1️⃣ Test OPTIONS (preflight):")
        options_response = requests.options(url, headers=headers, timeout=5)
        print(f"   Status: {options_response.status_code}")
        print(f"   CORS Headers: {dict(options_response.headers)}")
        
        # Test POST
        print("2️⃣ Test POST:")
        data = {
            "title": "Test CORS",
            "content": "Test de requête CORS",
            "subject": "Mathématiques",
            "chapter": "Test",
            "tags": "[\"cors\", \"test\"]",
            "color": "bg-blue-100"
        }
        
        post_response = requests.post(url, json=data, headers=headers, timeout=10)
        print(f"   Status: {post_response.status_code}")
        print(f"   Réponse: {post_response.text}")
        
        if post_response.status_code == 200:
            print("✅ Test CORS réussi!")
            return True
        else:
            print("❌ Test CORS échoué!")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du test CORS: {e}")
        return False

def check_frontend_config():
    """Vérifier la configuration du frontend"""
    print("\n🔍 Vérification de la configuration frontend...")
    
    # Vérifier si le frontend est en cours d'exécution
    try:
        response = requests.get("http://localhost:3001", timeout=5)
        print("✅ Frontend accessible sur http://localhost:3001")
    except:
        print("⚠️  Frontend non accessible sur http://localhost:3001")
        print("   Assurez-vous que le serveur frontend est démarré avec: npm run dev")
    
    # Vérifier la configuration de l'API
    api_config_path = "frontend/src/api/config.ts"
    if os.path.exists(api_config_path):
        print(f"✅ Fichier de configuration API trouvé: {api_config_path}")
    else:
        print(f"⚠️  Fichier de configuration API manquant: {api_config_path}")

def main():
    """Fonction principale de diagnostic"""
    print("🔧 Diagnostic de l'erreur 405 pour la création de notes")
    print("=" * 60)
    
    # 1. Démarrer le serveur backend
    if not start_server():
        print("\n❌ Impossible de démarrer le serveur backend")
        print("Solutions possibles:")
        print("1. Vérifiez que tous les modules Python sont installés")
        print("2. Vérifiez qu'il n'y a pas d'autres processus sur le port 8000")
        print("3. Redémarrez votre terminal et relancez le script")
        return
    
    # 2. Tester l'endpoint
    if not test_notes_endpoint():
        print("\n❌ L'endpoint de création de notes ne fonctionne pas")
        print("Solutions possibles:")
        print("1. Vérifiez que le fichier backend/api/v1/notes_advanced.py existe")
        print("2. Vérifiez que le router est correctement inclus dans app.py")
        print("3. Redémarrez le serveur backend")
        return
    
    # 3. Tester CORS
    if not test_cors():
        print("\n❌ Problème avec les requêtes CORS")
        print("Solutions possibles:")
        print("1. Vérifiez la configuration CORS dans backend/app.py")
        print("2. Assurez-vous que le frontend fait des requêtes depuis localhost:3001")
        return
    
    # 4. Vérifier la configuration frontend
    check_frontend_config()
    
    print("\n✅ Diagnostic terminé!")
    print("\n📋 Résumé:")
    print("- Backend: ✅ Fonctionnel")
    print("- Endpoint notes: ✅ Fonctionnel") 
    print("- CORS: ✅ Configuré correctement")
    print("\n🎯 Si vous avez encore l'erreur 405:")
    print("1. Ouvrez les outils de développement de votre navigateur (F12)")
    print("2. Allez dans l'onglet 'Network'")
    print("3. Essayez de créer une note")
    print("4. Vérifiez l'URL exacte de la requête et le status de la réponse")
    print("5. Assurez-vous que le frontend fait bien la requête vers http://localhost:8000/notes-advanced/")

if __name__ == "__main__":
    main() 