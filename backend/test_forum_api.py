#!/usr/bin/env python3
"""
Script pour tester l'API du forum
"""

import requests
import json
import sqlite3
import os
from datetime import datetime, timedelta
from jose import jwt

def generate_test_token():
    """Générer un JWT token de test"""
    
    # Configuration
    SECRET_KEY = "supersecret"  # Même clé que dans config.py
    ALGORITHM = "HS256"
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Trouver un utilisateur étudiant
        cursor.execute("SELECT id, email, first_name, last_name FROM users WHERE role = 'student' LIMIT 1")
        user = cursor.fetchone()
        
        if not user:
            print("❌ Aucun utilisateur étudiant trouvé")
            return None
            
        user_id, email, first_name, last_name = user
        print(f"👤 Utilisateur de test: {first_name} {last_name} ({email}) - ID: {user_id}")
        
        # Créer le payload du token
        payload = {
            "sub": email,  # Sujet du token (email de l'utilisateur)
            "user_id": user_id,
            "role": "student",
            "exp": datetime.utcnow() + timedelta(hours=1),  # Expire dans 1 heure
            "iat": datetime.utcnow()
        }
        
        # Générer le token
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        
        conn.close()
        return token, user_id
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du token: {e}")
        return None

def test_forum_api():
    """Tester l'API du forum"""
    
    base_url = "http://localhost:8000"
    
    # Obtenir un token de test
    auth_result = generate_test_token()
    if not auth_result:
        print("❌ Impossible d'obtenir un token d'authentification")
        return
        
    token, user_id = auth_result
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    print(f"\n🔑 Token JWT généré avec succès")
    print(f"🌐 Base URL: {base_url}")
    
    # Test 1: Récupérer les catégories
    print("\n📋 Test 1: Récupération des catégories")
    try:
        response = requests.get(f"{base_url}/api/v1/forum/categories", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            categories = response.json()
            print(f"✅ Catégories récupérées: {len(categories)}")
            for cat in categories[:3]:  # Afficher les 3 premières
                print(f"  - {cat.get('name', 'N/A')}: {cat.get('description', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des catégories: {e}")
    
    # Test 2: Récupérer les threads
    print("\n📝 Test 2: Récupération des threads")
    try:
        response = requests.get(f"{base_url}/api/v1/forum/threads", headers=headers)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            threads = response.json()
            print(f"✅ Threads récupérés: {len(threads)}")
            for thread in threads[:3]:  # Afficher les 3 premiers
                print(f"  - {thread.get('title', 'N/A')} par {thread.get('author', {}).get('name', 'N/A')}")
        else:
            print(f"❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test des threads: {e}")
    
    # Test 3: Créer un thread de test
    print("\n➕ Test 3: Création d'un thread de test")
    try:
        thread_data = {
            "title": "Test de création de thread",
            "content": "Ceci est un test de création de thread via l'API",
            "category_id": 1,  # Première catégorie
            "tags": "test,api,forum"
        }
        
        response = requests.post(f"{base_url}/api/v1/forum/threads", 
                               headers=headers, 
                               data=thread_data)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            thread = response.json()
            print(f"✅ Thread créé avec succès!")
            print(f"  - ID: {thread.get('id')}")
            print(f"  - Titre: {thread.get('title')}")
            print(f"  - Auteur: {thread.get('author', {}).get('name')}")
        else:
            print(f"❌ Erreur lors de la création: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur lors du test de création: {e}")

if __name__ == "__main__":
    print("🧪 Test de l'API du forum")
    print("=" * 50)
    
    test_forum_api()
    
    print("\n" + "=" * 50)
    print("🏁 Test terminé") 