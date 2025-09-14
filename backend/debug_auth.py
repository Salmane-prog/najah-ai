#!/usr/bin/env python3
"""
Script pour diagnostiquer le problème d'authentification
"""

import requests
import json
from jose import jwt

def debug_auth():
    print("=== DEBUG AUTHENTIFICATION ===")
    
    base_url = "http://localhost:8000"
    
    # Test 1: Récupérer le profil utilisateur
    print("\n🧪 Test 1: Récupérer le profil utilisateur")
    try:
        # Utiliser un token valide (copié depuis les logs du frontend)
        # Vous devez copier le token depuis la console du navigateur
        token = input("Entrez le token JWT depuis la console du navigateur: ").strip()
        
        if not token:
            print("❌ Aucun token fourni")
            return
        
        headers = {
            'Authorization': f'Bearer {token}',
            'Content-Type': 'application/json'
        }
        
        # Test de l'endpoint /me
        response = requests.get(f"{base_url}/api/v1/auth/me", headers=headers)
        print(f"Status /me: {response.status_code}")
        
        if response.status_code == 200:
            user_data = response.json()
            print(f"✅ Utilisateur connecté:")
            print(f"   - ID: {user_data.get('id')}")
            print(f"   - Email: {user_data.get('email')}")
            print(f"   - Rôle: {user_data.get('role')}")
            print(f"   - Nom: {user_data.get('first_name')} {user_data.get('last_name')}")
            
            # Test 2: Tester l'endpoint français avec ce token
            print(f"\n🧪 Test 2: Tester l'endpoint français")
            response_french = requests.post(
                f"{base_url}/api/v1/french/initial-assessment/student/start", 
                headers=headers
            )
            print(f"Status français: {response_french.status_code}")
            print(f"Response: {response_french.text}")
            
            # Test 3: Décoder le token JWT
            print(f"\n🧪 Test 3: Décoder le token JWT")
            try:
                # Note: On ne peut pas décoder sans la clé secrète, mais on peut voir la structure
                token_parts = token.split('.')
                if len(token_parts) == 3:
                    print(f"✅ Token JWT valide (3 parties)")
                    print(f"   - Header: {token_parts[0]}")
                    print(f"   - Payload: {token_parts[1]}")
                    print(f"   - Signature: {token_parts[2][:20]}...")
                else:
                    print(f"❌ Token JWT invalide: {len(token_parts)} parties")
            except Exception as e:
                print(f"❌ Erreur décodage token: {e}")
                
        else:
            print(f"❌ Erreur /me: {response.text}")
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    print("\n✅ Debug terminé")

if __name__ == "__main__":
    debug_auth()

