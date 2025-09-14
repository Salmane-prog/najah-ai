#!/usr/bin/env python3
"""
Script simple pour tester les endpoints analytics sans authentification
"""

import requests
import json

def test_endpoints_without_auth():
    """Tester les endpoints en contournant l'authentification temporairement"""
    
    # D'abord, testons si le serveur répond
    try:
        response = requests.get('http://localhost:8000/docs')
        print(f'✅ Serveur accessible: {response.status_code}')
    except Exception as e:
        print(f'❌ Serveur non accessible: {e}')
        return
    
    # Testons un endpoint simple d'abord
    try:
        response = requests.get('http://localhost:8000/api/v1/analytics/class-overview')
        print(f'📊 Test class-overview sans auth: {response.status_code}')
        if response.status_code == 200:
            data = response.json()
            print(f'   ✅ Données: {data}')
        else:
            print(f'   ❌ Erreur: {response.text}')
    except Exception as e:
        print(f'   ❌ Exception: {e}')

if __name__ == '__main__':
    test_endpoints_without_auth()