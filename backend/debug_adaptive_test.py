#!/usr/bin/env python3
"""
Script de débogage pour l'endpoint de création de test adaptatif
"""

import requests
import json
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
API_ENDPOINT = f"{BASE_URL}/api/v1/adaptive-evaluation/tests/"

def debug_adaptive_test():
    """Débogage complet de l'endpoint"""
    
    print("🔍 Débogage de l'endpoint de création de test adaptatif")
    print("=" * 60)
    
    # 1. Vérifier l'état du serveur
    print("1️⃣ Vérification de l'état du serveur...")
    try:
        response = requests.get(f"{BASE_URL}/docs")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   ✅ Serveur accessible")
        else:
            print(f"   ⚠️ Serveur répond avec status {response.status_code}")
    except Exception as e:
        print(f"   ❌ Serveur inaccessible: {e}")
        return False
    
    # 2. Vérifier l'endpoint sans authentification
    print("\n2️⃣ Test de l'endpoint sans authentification...")
    try:
        response = requests.post(API_ENDPOINT, json={})
        print(f"   Status: {response.status_code}")
        if response.status_code == 401:
            print("   ✅ Endpoint protégé (401 attendu)")
        elif response.status_code == 403:
            print("   ⚠️ Endpoint retourne 403 sans authentification (inattendu)")
        else:
            print(f"   ⚠️ Status inattendu: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 3. Connexion et récupération du token
    print("\n3️⃣ Connexion et récupération du token...")
    login_data = {
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=login_data)
        print(f"   Status: {login_response.status_code}")
        
        if login_response.status_code == 200:
            token_data = login_response.json()
            access_token = token_data.get("access_token")
            user_role = token_data.get("role")
            user_id = token_data.get("id")
            print(f"   ✅ Connexion réussie")
            print(f"   🔑 Token: {access_token[:50]}...")
            print(f"   👤 Rôle: {user_role}")
            print(f"   🆔 ID: {user_id}")
        else:
            print(f"   ❌ Échec de la connexion: {login_response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la connexion: {e}")
        return False
    
    # 4. Vérifier les informations de l'utilisateur
    print("\n4️⃣ Vérification des informations utilisateur...")
    headers = {"Authorization": f"Bearer {access_token}"}
    
    try:
        me_response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
        print(f"   Status: {me_response.status_code}")
        
        if me_response.status_code == 200:
            user_info = me_response.json()
            print(f"   ✅ Informations utilisateur récupérées")
            print(f"   📋 Rôle: {user_info.get('role')}")
            print(f"   📋 Email: {user_info.get('email')}")
            print(f"   📋 ID: {user_info.get('id')}")
        else:
            print(f"   ❌ Erreur lors de la récupération des infos: {me_response.text}")
            
    except Exception as e:
        print(f"   ❌ Erreur: {e}")
    
    # 5. Test de création avec données minimales
    print("\n5️⃣ Test de création avec données minimales...")
    
    minimal_test_data = {
        "title": "Test Debug - Français",
        "subject": "Français",
        "description": "Test de débogage",
        "difficulty_min": 1,
        "difficulty_max": 5,
        "estimated_duration": 15,
        "total_questions": 5,
        "adaptation_type": "hybrid",
        "learning_objectives": "Test de débogage"
    }
    
    try:
        print(f"   📤 Envoi de la requête...")
        print(f"   📋 Données: {json.dumps(minimal_test_data, indent=2)}")
        
        response = requests.post(API_ENDPOINT, json=minimal_test_data, headers=headers)
        
        print(f"\n   📥 Réponse reçue:")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Body: {response.text}")
        
        if response.status_code == 200:
            print("   ✅ Test créé avec succès !")
            return True
        elif response.status_code == 403:
            print("   ❌ Erreur 403: Accès refusé")
            print("   💡 Problème d'autorisation malgré l'authentification")
            return False
        elif response.status_code == 401:
            print("   ❌ Erreur 401: Non authentifié")
            print("   💡 Problème avec le token")
            return False
        else:
            print(f"   ❌ Erreur {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"   ❌ Erreur lors de la requête: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Démarrage du débogage")
    print(f"📍 URL de test: {API_ENDPOINT}")
    print(f"⏰ Heure: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = debug_adaptive_test()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Débogage terminé avec succès !")
    else:
        print("❌ Débogage terminé avec des erreurs")
    
    print("�� Fin du débogage")










