#!/usr/bin/env python3
"""
Script final pour tester les endpoints analytics avec authentification
"""

import requests
import jwt
import datetime
import json

def create_token():
    """Créer un token JWT valide pour un utilisateur existant"""
    secret_key = 'supersecret'
    
    # Utiliser un utilisateur existant de la base de données
    payload = {
        'sub': 'teacher1@najah.ai',  # Email d'un utilisateur existant
        'user_id': 2,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    return jwt.encode(payload, secret_key, algorithm='HS256')

def test_endpoint(endpoint, token):
    """Tester un endpoint spécifique"""
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(f'http://localhost:8000{endpoint}', headers=headers)
        print(f'📊 {endpoint}: {response.status_code}')
        
        if response.status_code == 200:
            data = response.json()
            print(f'   ✅ Données: {len(data)} éléments')
            if data and len(data) > 0:
                print(f'   📋 Premier élément: {json.dumps(data[0], indent=2)[:200]}...')
            return True
        else:
            print(f'   ❌ Erreur: {response.text[:200]}')
            return False
    except Exception as e:
        print(f'   ❌ Exception: {e}')
        return False

def main():
    print('🧪 Test final des endpoints analytics...')
    
    # Créer un token
    token = create_token()
    print(f'🔑 Token créé: {token[:50]}...')
    
    # Endpoints à tester
    endpoints = [
        '/api/v1/analytics/class-overview',
        '/api/v1/analytics/weekly-progress',
        '/api/v1/analytics/monthly-stats',
        '/api/v1/analytics/difficulty-performance',
        '/api/v1/analytics/engagement-trends',
        '/api/v1/analytics/score-distribution',
        '/api/v1/analytics/learning-trends',
        '/api/v1/analytics/ai-predictions',
        '/api/v1/analytics/learning-blockages'
    ]
    
    success_count = 0
    for endpoint in endpoints:
        if test_endpoint(endpoint, token):
            success_count += 1
        print()
    
    print(f'📈 Résultat final: {success_count}/{len(endpoints)} endpoints fonctionnent')
    
    if success_count == 0:
        print('❌ Aucun endpoint ne fonctionne. Vérifiez:')
        print('   1. Le serveur backend est-il en cours d\'exécution ?')
        print('   2. L\'utilisateur teacher1@najah.ai existe-t-il ?')
        print('   3. Y a-t-il des erreurs dans les logs du serveur ?')

if __name__ == '__main__':
    main()








