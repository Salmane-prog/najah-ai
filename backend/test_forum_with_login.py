#!/usr/bin/env python3
"""
Test de l'API du forum avec authentification réelle
"""

import urllib.request
import urllib.parse
import json
import sqlite3
import os

def get_test_user_credentials():
    """Obtenir les identifiants d'un utilisateur de test"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Trouver un utilisateur étudiant
        cursor.execute("SELECT id, email, username, hashed_password FROM users WHERE role = 'student' LIMIT 1")
        user = cursor.fetchone()
        
        if not user:
            print("❌ Aucun utilisateur étudiant trouvé")
            return None
            
        user_id, email, username, hashed_password = user
        print(f"👤 Utilisateur trouvé: {username} ({email}) - ID: {user_id}")
        
        # Pour le test, utilisons un mot de passe simple
        # En production, il faudrait utiliser le vrai mot de passe
        test_password = "password123"  # Mot de passe de test
        
        conn.close()
        return email, test_password, user_id
        
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de l'utilisateur: {e}")
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

def login_and_test_forum():
    """Se connecter et tester l'API du forum"""
    
    base_url = "http://localhost:8000"
    
    # Obtenir les identifiants de test
    credentials = get_test_user_credentials()
    if not credentials:
        print("❌ Impossible d'obtenir les identifiants de test")
        return
        
    email, password, user_id = credentials
    print(f"\n🔐 Tentative de connexion avec {email}")
    
    # Étape 1: Se connecter pour obtenir un token
    print("\n📝 Étape 1: Connexion")
    login_data = {
        "email": email,
        "password": password
    }
    
    login_json = json.dumps(login_data)
    login_url = f"{base_url}/api/v1/auth/login"
    
    print(f"URL de connexion: {login_url}")
    print(f"Données: {login_data}")
    
    status, content = make_request(login_url, method="POST", data=login_json)
    print(f"Status de connexion: {status}")
    
    if status != 200:
        print(f"❌ Échec de la connexion: {content}")
        return None
    
    try:
        login_response = json.loads(content)
        token = login_response.get('access_token')
        
        if not token:
            print("❌ Aucun token reçu dans la réponse")
            return None
            
        print(f"✅ Connexion réussie!")
        print(f"🔑 Token reçu: {token[:20]}...")
        print(f"👤 Rôle: {login_response.get('role')}")
        
        return token
        
    except json.JSONDecodeError:
        print(f"❌ Erreur de décodage de la réponse: {content}")
        return None

def test_forum_endpoints(token):
    """Tester les endpoints du forum avec le token"""
    
    base_url = "http://localhost:8000"
    
    print(f"\n🧪 Test des endpoints du forum")
    print(f"🌐 Base URL: {base_url}")
    
    # Test 1: Endpoint de test (sans authentification)
    print("\n📋 Test 1: Endpoint de test (sans auth)")
    url = f"{base_url}/api/v1/forum/test"
    status, content = make_request(url)
    
    print(f"URL: {url}")
    print(f"Status: {status}")
    
    if status == 200:
        try:
            response = json.loads(content)
            print(f"✅ Test réussi: {response.get('message')}")
        except json.JSONDecodeError:
            print(f"❌ Erreur de décodage JSON: {content}")
    else:
        print(f"❌ Erreur: {content}")
    
    # Test 2: Récupérer les catégories (avec authentification)
    print("\n📋 Test 2: Récupération des catégories (avec auth)")
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
    
    # Test 3: Récupérer les threads (avec authentification)
    print("\n📝 Test 3: Récupération des threads (avec auth)")
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
    
    # Test 4: Créer un thread de test (avec authentification)
    print("\n➕ Test 4: Création d'un thread de test (avec auth)")
    url = f"{base_url}/api/v1/forum/threads"
    
    thread_data = {
        "title": "Test de création de thread via API",
        "content": "Ceci est un test de création de thread via l'API avec authentification réelle",
        "category_id": 1,  # Première catégorie
        "tags": "test,api,forum,auth"
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
    print("🧪 Test de l'API du forum avec authentification réelle")
    print("=" * 60)
    
    # Étape 1: Se connecter
    token = login_and_test_forum()
    
    if token:
        # Étape 2: Tester les endpoints
        test_forum_endpoints(token)
    else:
        print("\n❌ Impossible de se connecter, arrêt des tests")
    
    print("\n" + "=" * 60)
    print("🏁 Test terminé")

