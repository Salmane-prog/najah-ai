#!/usr/bin/env python3
"""
Script de test pour les endpoints analytics modifiés
"""

import requests
import jwt
import datetime
import json

def create_token(email, user_id):
    """Créer un token JWT valide"""
    secret_key = 'supersecret'
    payload = {
        'sub': email,
        'user_id': user_id,
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
            print(f'   ✅ Données: {json.dumps(data, indent=2)[:200]}...')
            return True
        else:
            print(f'   ❌ Erreur: {response.text}')
            return False
    except Exception as e:
        print(f'   ❌ Exception: {e}')
        return False

def main():
    print('🧪 Test des endpoints analytics modifiés...')
    
    # Créer un token pour un professeur
    token = create_token('teacher1@najah.ai', 2)
    print(f'🔑 Token généré: {token[:50]}...')
    
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
    
    print(f'📈 Résultat: {success_count}/{len(endpoints)} endpoints fonctionnent')

if __name__ == '__main__':
    main()