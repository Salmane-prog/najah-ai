#!/usr/bin/env python3
"""
Test simple de l'API du forum sans dépendances externes
"""

import urllib.request
import urllib.parse
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
        print(f"👤 Utilisateur: {first_name} {last_name} ({email}) - ID: {user_id}")
        
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
        return token, email
        
    except Exception as e:
        print(f"❌ Erreur lors de la génération du token: {e}")
        return None

def make_request(url, method="GET", data=None, token=None):
    """Faire une requête HTTP simple"""
    
    headers = {
        'Content-Type': 'application/json',
    }
    
    if token:
        headers['Authorization'] = f'Bearer {token}'
    
    try:
        if method == "GET":
            req = urllib.request.Request(url, headers=headers)
        else:
            req = urllib.request.Request(url, data=data.encode('utf-8') if data else None, headers=headers, method=method)
        
        with urllib.request.urlopen(req) as response:
            status = response.getcode()
            content = response.read().decode('utf-8')
            return status, content
            
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode('utf-8')
    except Exception as e:
        return None, str(e)

def test_forum_api():
    """Tester l'API du forum"""
    
    base_url = "http://localhost:8000"
    
    # Obtenir un token de test
    auth_result = generate_test_token()
    if not auth_result:
        print("❌ Impossible d'obtenir un token d'authentification")
        return
        
    token, email = auth_result
    print(f"\n🔑 Token JWT généré avec succès pour {email}")
    print(f"🌐 Base URL: {base_url}")
    
    # Test 1: Récupérer les catégories
    print("\n📋 Test 1: Récupération des catégories")
    url = f"{base_url}/api/v1/forum/categories"
    status, content = make_request(url, token=token)
    
    print(f"URL: {url}")
    print(f"Status: {status}")
    
    if status == 200:
        try:
            categories = json.loads(content)
            print(f"✅ Catégories récupérées: {len(categories)}")
            for cat in categories[:3]:  # Afficher les 3 premières
                print(f"  - {cat.get('name', 'N/A')}: {cat.get('description', 'N/A')}")
        except json.JSONDecodeError:
            print(f"❌ Erreur de décodage JSON: {content}")
    else:
        print(f"❌ Erreur: {content}")
    
    # Test 2: Récupérer les threads
    print("\n📝 Test 2: Récupération des threads")
    url = f"{base_url}/api/v1/forum/threads"
    status, content = make_request(url, token=token)
    
    print(f"URL: {url}")
    print(f"Status: {status}")
    
    if status == 200:
        try:
            threads = json.loads(content)
            print(f"✅ Threads récupérés: {len(threads)}")
            for thread in threads[:3]:  # Afficher les 3 premiers
                print(f"  - {thread.get('title', 'N/A')} par {thread.get('author', {}).get('name', 'N/A')}")
        except json.JSONDecodeError:
            print(f"❌ Erreur de décodage JSON: {content}")
    else:
        print(f"❌ Erreur: {content}")
    
    # Test 3: Créer un thread de test
    print("\n➕ Test 3: Création d'un thread de test")
    url = f"{base_url}/api/v1/forum/threads"
    
    thread_data = {
        "title": "Test de création de thread",
        "content": "Ceci est un test de création de thread via l'API",
        "category_id": 1,  # Première catégorie
        "tags": "test,api,forum"
    }
    
    data_json = json.dumps(thread_data)
    status, content = make_request(url, method="POST", data=data_json, token=token)
    
    print(f"URL: {url}")
    print(f"Status: {status}")
    print(f"Data envoyée: {thread_data}")
    
    if status == 201:
        try:
            thread = json.loads(content)
            print(f"✅ Thread créé avec succès!")
            print(f"  - ID: {thread.get('id')}")
            print(f"  - Titre: {thread.get('title')}")
            print(f"  - Auteur: {thread.get('author', {}).get('name')}")
        except json.JSONDecodeError:
            print(f"❌ Erreur de décodage JSON: {content}")
    else:
        print(f"❌ Erreur lors de la création: {content}")

if __name__ == "__main__":
    print("🧪 Test simple de l'API du forum")
    print("=" * 50)
    
    test_forum_api()
    
    print("\n" + "=" * 50)
    print("🏁 Test terminé")

