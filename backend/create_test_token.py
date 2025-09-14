#!/usr/bin/env python3
"""
Script pour créer un token d'authentification valide pour tester les endpoints
"""

import jwt
from datetime import datetime, timedelta
from core.security import SECRET_KEY, ALGORITHM

def create_test_token():
    """Crée un token de test valide pour l'utilisateur student1 (ID: 4)"""
    
    # Données du token
    payload = {
        "sub": "student1@test.com",  # email de l'utilisateur
        "user_id": 4,                # ID de student1
        "role": "student",           # Rôle de l'utilisateur
        "exp": datetime.utcnow() + timedelta(hours=24),  # Expire dans 24h
        "iat": datetime.utcnow()     # Issued at
    }
    
    # Créer le token
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    
    print("🔑 TOKEN D'AUTHENTIFICATION CRÉÉ")
    print("=" * 50)
    print(f"Token: {token}")
    print("\n📋 UTILISATION:")
    print("1. Copiez ce token")
    print("2. Dans votre frontend, ajoutez-le dans le localStorage:")
    print("   localStorage.setItem('token', 'VOTRE_TOKEN_ICI')")
    print("3. Ou utilisez-le dans vos tests API:")
    print("   Authorization: Bearer VOTRE_TOKEN_ICI")
    print("\n👤 UTILISATEUR:")
    print(f"   ID: {payload['user_id']}")
    print(f"   Email: {payload['sub']}")
    print(f"   Rôle: {payload['role']}")
    print(f"   Expire: {payload['exp']}")
    
    return token

def test_endpoints_with_token(token):
    """Teste les endpoints avec le token créé"""
    
    import requests
    
    base_url = "http://localhost:8000"
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\n🧪 TEST DES ENDPOINTS AVEC AUTHENTIFICATION")
    print("=" * 50)
    
    # Endpoints à tester
    endpoints = [
        "/api/v1/badges/",
        "/api/v1/ai-advanced/recommendations",
        "/api/v1/reports/detailed",
        "/api/v1/reports/analytics",
        "/api/v1/reports/subject-progress",
        "/api/v1/homework/",
        "/api/v1/ai-advanced/tutoring/sessions",
        "/api/v1/ai-advanced/difficulty-detection"
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f"{base_url}{endpoint}", headers=headers)
            if response.status_code == 200:
                data = response.json()
                print(f"✅ {endpoint}: 200 OK - {len(data) if isinstance(data, list) else 'Object'} éléments")
            else:
                print(f"⚠️  {endpoint}: {response.status_code} - {response.text[:100]}")
        except Exception as e:
            print(f"❌ {endpoint}: Erreur - {str(e)[:100]}")

if __name__ == "__main__":
    print("🔑 CRÉATION DE TOKEN D'AUTHENTIFICATION")
    print("=" * 50)
    
    # Créer le token
    token = create_test_token()
    
    # Tester les endpoints
    test_endpoints_with_token(token)
    
    print("\n" + "=" * 50)
    print("🎯 PROCHAINES ÉTAPES:")
    print("1. Utilisez ce token dans votre frontend")
    print("2. Les erreurs 'Failed to fetch' devraient disparaître")
    print("3. Les données réelles devraient s'afficher")
    print("4. Toutes les pages devraient être synchronisées")


