#!/usr/bin/env python3
"""
Script de test pour l'authentification
"""

import requests

def test_login():
    """Tester la connexion avec différents mots de passe"""
    passwords = ['password', '123456', 'admin', 'teacher1', 'prof_math']
    
    for pwd in passwords:
        try:
            response = requests.post('http://localhost:8000/api/v1/auth/login', 
                                   json={'email': 'teacher1@najah.ai', 'password': pwd})
            print(f'🔐 Test avec mot de passe "{pwd}": {response.status_code}')
            if response.status_code == 200:
                data = response.json()
                token = data.get('access_token', 'N/A')
                print(f'   ✅ Succès! Token: {token[:50]}...')
                return token
            else:
                print(f'   ❌ Erreur: {response.text[:100]}')
        except Exception as e:
            print(f'   ❌ Exception: {e}')
        print()
    
    return None

def test_analytics_with_token(token):
    """Tester les endpoints analytics avec un token valide"""
    if not token:
        print('❌ Aucun token valide disponible')
        return
    
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    endpoints = [
        '/api/v1/analytics/class-overview',
        '/api/v1/analytics/weekly-progress',
        '/api/v1/analytics/monthly-stats'
    ]
    
    for endpoint in endpoints:
        try:
            response = requests.get(f'http://localhost:8000{endpoint}', headers=headers)
            print(f'📊 {endpoint}: {response.status_code}')
            if response.status_code == 200:
                data = response.json()
                print(f'   ✅ Données: {data}')
            else:
                print(f'   ❌ Erreur: {response.text}')
        except Exception as e:
            print(f'   ❌ Exception: {e}')
        print()

def main():
    print('🧪 Test d\'authentification et analytics...')
    
    # Tester la connexion
    token = test_login()
    
    if token:
        print('\\n🧪 Test des endpoints analytics...')
        test_analytics_with_token(token)
    else:
        print('❌ Impossible de se connecter')

if __name__ == '__main__':
    main()