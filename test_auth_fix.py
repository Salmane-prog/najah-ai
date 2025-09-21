#!/usr/bin/env python3
"""
Script de test pour vérifier que les corrections d'authentification fonctionnent
"""

import requests
import json
import time

def test_backend_health():
    """Tester la santé du backend"""
    print("🔍 Test de la santé du backend...")
    try:
        response = requests.get('http://localhost:8000/health', timeout=10)
        if response.status_code == 200:
            print("✅ Backend opérationnel")
            return True
        else:
            print(f"❌ Backend répond avec le code {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Backend inaccessible: {e}")
        return False

def test_login():
    """Tester la connexion et obtenir un token"""
    print("\n🔐 Test de connexion...")
    
    login_data = {
        "username": "student@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            'http://localhost:8000/api/v1/auth/login',
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            data = response.json()
            token = data.get('access_token')
            print("✅ Connexion réussie")
            print(f"   Token obtenu: {token[:50]}...")
            return token
        else:
            print(f"❌ Échec de la connexion: {response.status_code}")
            print(f"   Réponse: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Erreur lors de la connexion: {e}")
        return None

def test_protected_endpoints(token):
    """Tester les endpoints protégés"""
    print("\n🛡️ Test des endpoints protégés...")
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    endpoints = [
        ('/api/v1/students/30/study-sessions', 'Sessions d\'étude'),
        ('/api/v1/students/30/learning-goals', 'Objectifs d\'apprentissage'),
        ('/api/v1/assignments/homework/assigned/30', 'Devoirs assignés')
    ]
    
    results = []
    
    for endpoint, name in endpoints:
        try:
            response = requests.get(
                f'http://localhost:8000{endpoint}',
                headers=headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {name}: {len(data) if isinstance(data, list) else 'OK'}")
                results.append(True)
            elif response.status_code == 401:
                print(f"❌ {name}: Token expiré (401)")
                results.append(False)
            else:
                print(f"⚠️ {name}: Code {response.status_code}")
                results.append(False)
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {name}: Erreur de connexion - {e}")
            results.append(False)
    
    return results

def test_token_expiration():
    """Tester l'expiration du token"""
    print("\n⏰ Test de l'expiration du token...")
    
    # Obtenir un token
    token = test_login()
    if not token:
        print("❌ Impossible de tester l'expiration sans token")
        return False
    
    # Décoder le token pour voir l'expiration
    try:
        import base64
        payload = json.loads(base64.b64decode(token.split('.')[1] + '=='))
        exp_time = payload.get('exp', 0)
        current_time = time.time()
        
        print(f"   Token expirera dans: {int(exp_time - current_time)} secondes")
        
        if exp_time > current_time + 3600:  # Plus d'1 heure
            print("✅ Token valide pour plus d'1 heure")
            return True
        else:
            print("⚠️ Token expire bientôt")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors du décodage du token: {e}")
        return False

def main():
    print("🧪 Test des corrections d'authentification")
    print("=" * 50)
    
    # 1. Tester la santé du backend
    if not test_backend_health():
        print("\n❌ Backend non disponible, arrêt des tests")
        return
    
    # 2. Tester la connexion
    token = test_login()
    if not token:
        print("\n❌ Impossible de se connecter, arrêt des tests")
        return
    
    # 3. Tester les endpoints protégés
    results = test_protected_endpoints(token)
    
    # 4. Tester l'expiration du token
    token_valid = test_token_expiration()
    
    # Résumé
    print("\n📊 Résumé des tests:")
    print(f"   Backend opérationnel: ✅")
    print(f"   Connexion réussie: {'✅' if token else '❌'}")
    print(f"   Endpoints protégés: {sum(results)}/{len(results)} fonctionnels")
    print(f"   Token valide: {'✅' if token_valid else '❌'}")
    
    if all(results) and token_valid:
        print("\n🎉 Tous les tests sont passés! Les corrections fonctionnent.")
    else:
        print("\n⚠️ Certains tests ont échoué. Vérifiez les logs du backend.")

if __name__ == "__main__":
    main()








