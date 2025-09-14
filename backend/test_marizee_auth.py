#!/usr/bin/env python3
"""
Script pour tester l'authentification avec Marizee Dubois
"""

import requests
import json

def test_marizee_login():
    """Teste la connexion avec Marizee Dubois"""
    
    print("🧪 Test d'authentification avec Marizee Dubois")
    print("=" * 60)
    
    # Données de connexion
    login_data = {
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        print(f"🔐 Tentative de connexion...")
        print(f"   Email: {login_data['email']}")
        print(f"   Mot de passe: {login_data['password']}")
        
        # Appel à l'API de connexion
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data
        )
        
        print(f"\n📊 Réponse de l'API :")
        print(f"   Status: {response.status_code}")
        print(f"   Headers: {dict(response.headers)}")
        print(f"   Body: {response.text}")
        
        if response.status_code == 200:
            data = response.json()
            token = data.get("access_token")
            print(f"\n✅ CONNEXION RÉUSSIE !")
            print(f"   Token: {token[:50]}...")
            
            # Tester le token avec l'endpoint protégé
            print(f"\n🔍 Test de l'endpoint protégé...")
            headers = {"Authorization": f"Bearer {token}"}
            
            test_response = requests.post(
                "http://localhost:8000/api/v1/ai-formative-evaluations/generate-evaluation/",
                headers=headers,
                json={
                    "title": "Test d'évaluation formative",
                    "subject": "Mathématiques",
                    "assessment_type": "project",
                    "description": "Test de génération d'évaluation formative avec l'IA",
                    "target_level": "intermediate",
                    "duration_minutes": 60,
                    "max_students": 30,
                    "learning_objectives": ["Compétence 1", "Compétence 2"],
                    "custom_requirements": "Aucune"
                }
            )
            
            print(f"\n📊 Test endpoint protégé :")
            print(f"   Status: {test_response.status_code}")
            print(f"   Headers: {dict(test_response.headers)}")
            print(f"   Body: {test_response.text}")
            
            if test_response.status_code == 200:
                print(f"\n🎉 SUCCÈS COMPLET ! L'API fonctionne parfaitement !")
                print(f"   L'erreur 'Générer avec l'IA' est maintenant résolue !")
                return token
            else:
                print(f"\n❌ Endpoint protégé échoue")
                print(f"   Erreur: {test_response.text}")
                return None
                
        else:
            print(f"\n❌ ÉCHEC DE LA CONNEXION")
            print(f"   Erreur: {response.text}")
            return None
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return None

if __name__ == "__main__":
    print("🔐 Test d'authentification avec Marizee Dubois")
    print("=" * 80)
    
    # Tester la connexion
    token = test_marizee_login()
    
    if token:
        print(f"\n🎯 AUTHENTIFICATION RÉUSSIE !")
        print(f"Token valide: {token[:50]}...")
        print(f"\n🔧 POUR TESTER LE FRONTEND :")
        print(f"1. Ouvre la console du navigateur (F12)")
        print(f"2. Exécute cette commande :")
        print(f"   localStorage.setItem('najah_token', '{token}')")
        print(f"3. Rafraîchis la page")
        print(f"4. Va sur 'Évaluations Formatives'")
        print(f"5. Clique sur 'Générer avec l'IA'")
        print(f"6. L'erreur devrait être résolue ! 🎉")
    else:
        print(f"\n❌ ÉCHEC ! L'authentification n'a pas fonctionné")
        print(f"🔍 Vérification nécessaire de la configuration")















