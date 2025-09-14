#!/usr/bin/env python3
"""
Script pour tester l'endpoint /list avec authentification
"""

import requests
import json

def test_authenticated_endpoint():
    """Teste l'endpoint /list avec authentification"""
    
    base_url = "http://localhost:8000"
    
    print("🧪 Test de l'endpoint /list avec authentification...")
    print("=" * 60)
    
    # 1. Se connecter pour obtenir un token
    print("\n1️⃣ Connexion pour obtenir un token...")
    
    login_data = {
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        response = requests.post(f"{base_url}/api/v1/auth/login", json=login_data)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print(f"   ✅ Token obtenu: {access_token[:50]}...")
        else:
            print(f"   ❌ Erreur de connexion: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
        return False
    
    # 2. Tester l'endpoint /list avec le token
    print("\n2️⃣ Test de l'endpoint /list avec authentification...")
    
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        response = requests.get(f"{base_url}/api/v1/adaptive-evaluations/list", headers=headers)
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Réponse reçue!")
            print(f"   Tests adaptatifs: {len(data.get('adaptive_tests', []))}")
            print(f"   Évaluations formatives: {len(data.get('formative_evaluations', []))}")
            
            # Afficher les détails
            if data.get('adaptive_tests'):
                print(f"\n   Tests adaptatifs trouvés:")
                for test in data['adaptive_tests']:
                    print(f"     - {test['title']} ({test['subject']}) - {test['assigned_students']} étudiants")
            
            if data.get('formative_evaluations'):
                print(f"\n   Évaluations formatives trouvées:")
                for eval in data['formative_evaluations']:
                    print(f"     - {eval['title']} ({eval['subject']}) - {eval['assigned_students']} étudiants")
                    
        else:
            print(f"   ❌ Erreur: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    # 3. Tester l'endpoint sans token (devrait échouer)
    print("\n3️⃣ Test de l'endpoint /list sans token...")
    
    try:
        response = requests.get(f"{base_url}/api/v1/adaptive-evaluations/list")
        print(f"   Status: {response.status_code}")
        
        if response.status_code == 401:
            print(f"   ✅ Attendu: 401 Unauthorized")
        else:
            print(f"   ⚠️  Status inattendu: {response.status_code}")
            print(f"   Réponse: {response.text}")
            
    except Exception as e:
        print(f"   ❌ Exception: {str(e)}")
    
    print("\n" + "=" * 60)
    print("🎯 Résumé:")
    print("   - Si le test 1 fonctionne: Connexion OK ✅")
    print("   - Si le test 2 fonctionne: Endpoint /list OK ✅")
    print("   - Si le test 3 retourne 401: Authentification OK ✅")
    print("   - Si vous obtenez 403: Problème d'autorisation ❌")

if __name__ == "__main__":
    test_authenticated_endpoint()
