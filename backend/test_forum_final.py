#!/usr/bin/env python3
"""
Test final de l'API du forum
"""

import urllib.request
import json
import sqlite3
import os

def get_test_user_credentials():
    """Obtenir les identifiants d'un utilisateur de test"""
    
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT id, email, username FROM users WHERE role = 'student' LIMIT 1")
        user = cursor.fetchone()
        
        if not user:
            print("❌ Aucun utilisateur étudiant trouvé")
            return None
            
        user_id, email, username = user
        print(f"👤 Utilisateur: {username} ({email}) - ID: {user_id}")
        
        test_password = "password123"
        conn.close()
        return email, test_password
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
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
    
    # 1. Se connecter
    print("🔐 Étape 1: Connexion")
    credentials = get_test_user_credentials()
    if not credentials:
        return
        
    email, password = credentials
    
    login_data = {"email": email, "password": password}
    login_json = json.dumps(login_data)
    
    status, content = make_request(f"{base_url}/api/v1/auth/login", method="POST", data=login_json)
    
    if status != 200:
        print(f"❌ Échec de la connexion: {content}")
        return
        
    try:
        login_response = json.loads(content)
        token = login_response.get('access_token')
        print(f"✅ Connexion réussie! Token: {token[:20]}...")
    except json.JSONDecodeError:
        print(f"❌ Erreur de décodage: {content}")
        return
    
    # 2. Tester les catégories
    print("\n📋 Étape 2: Test des catégories")
    status, content = make_request(f"{base_url}/api/v1/forum/categories", token=token)
    
    if status == 200:
        try:
            categories = json.loads(content)
            print(f"✅ {len(categories)} catégories récupérées")
            for cat in categories[:3]:
                print(f"  - {cat.get('name')}: {cat.get('description')}")
        except json.JSONDecodeError:
            print(f"❌ Erreur JSON: {content}")
    else:
        print(f"❌ Erreur catégories: {content}")
    
    # 3. Tester la création de thread
    print("\n➕ Étape 3: Test de création de thread")
    thread_data = {
        "title": "Test de création via API corrigée",
        "content": "Ceci est un test de création de thread avec la nouvelle API corrigée",
        "category_id": 1,
        "tags": "test,api,corrigé"
    }
    
    thread_json = json.dumps(thread_data)
    status, content = make_request(f"{base_url}/api/v1/forum/threads", method="POST", data=thread_json, token=token)
    
    print(f"Status: {status}")
    print(f"Data envoyée: {thread_data}")
    
    if status == 201:
        try:
            thread = json.loads(content)
            print(f"✅ Thread créé avec succès!")
            print(f"  - ID: {thread.get('id')}")
            print(f"  - Titre: {thread.get('title')}")
        except json.JSONDecodeError:
            print(f"❌ Erreur JSON: {content}")
    else:
        print(f"❌ Erreur création: {content}")
    
    # 4. Tester la récupération des threads
    print("\n📝 Étape 4: Test de récupération des threads")
    status, content = make_request(f"{base_url}/api/v1/forum/threads", token=token)
    
    if status == 200:
        try:
            threads = json.loads(content)
            print(f"✅ {len(threads)} threads récupérés")
            for thread in threads[:3]:
                print(f"  - {thread.get('title')} par {thread.get('author', {}).get('name', 'N/A')}")
        except json.JSONDecodeError:
            print(f"❌ Erreur JSON: {content}")
    else:
        print(f"❌ Erreur threads: {content}")

if __name__ == "__main__":
    print("🧪 Test final de l'API du forum")
    print("=" * 50)
    
    test_forum_api()
    
    print("\n" + "=" * 50)
    print("🏁 Test terminé")

