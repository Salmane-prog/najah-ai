#!/usr/bin/env python3
"""
Script pour tester la récupération des évaluations formatives
"""

import requests
import json

def test_retrieve_evaluations():
    """Teste la récupération des évaluations formatives"""
    
    print("🧪 Test de récupération des évaluations formatives")
    print("=" * 70)
    
    # ÉTAPE 1 : Connexion
    print("\n🔐 ÉTAPE 1 : Connexion...")
    
    login_data = {
        "email": "marizee.dubois@najah.ai",
        "password": "password123"
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/v1/auth/login",
            json=login_data
        )
        
        if response.status_code != 200:
            print(f"❌ Échec de la connexion: {response.text}")
            return None
        
        data = response.json()
        token = data.get("access_token")
        print(f"✅ Connexion réussie ! Token: {token[:50]}...")
        
        # ÉTAPE 2 : Récupération des évaluations
        print("\n📚 ÉTAPE 2 : Récupération des évaluations...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        retrieve_response = requests.get(
            "http://localhost:8000/api/v1/formative-evaluations/",
            headers=headers
        )
        
        print(f"\n📊 Réponse de récupération:")
        print(f"   Status: {retrieve_response.status_code}")
        print(f"   Headers: {dict(retrieve_response.headers)}")
        print(f"   Body: {retrieve_response.text}")
        
        if retrieve_response.status_code == 200:
            evaluations = retrieve_response.json()
            print(f"\n🎉 SUCCÈS ! Évaluations récupérées !")
            print(f"   Nombre d'évaluations: {len(evaluations)}")
            
            for i, eval in enumerate(evaluations):
                print(f"\n   📋 Évaluation {i+1}:")
                print(f"      ID: {eval.get('id')}")
                print(f"      Titre: {eval.get('title')}")
                print(f"      Sujet: {eval.get('subject')}")
                print(f"      Type: {eval.get('assessment_type')}")
                print(f"      Créée par: {eval.get('teacher_id')}")
                print(f"      Date: {eval.get('created_at')}")
            
            return True
        else:
            print(f"\n❌ ÉCHEC DE LA RÉCUPÉRATION")
            print(f"   Erreur: {retrieve_response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Test de récupération des évaluations formatives")
    print("=" * 80)
    
    success = test_retrieve_evaluations()
    
    if success:
        print(f"\n✅ RÉCUPÉRATION RÉUSSIE !")
        print(f"   Les évaluations s'afficheront maintenant dans le frontend !")
        print(f"\n🔧 POUR TESTER LE FRONTEND :")
        print(f"1. Rafraîchis la page frontend")
        print(f"2. Va sur 'Évaluations Formatives'")
        print(f"3. Tu devrais voir tes évaluations ! 🎉")
    else:
        print(f"\n❌ ÉCHEC ! La récupération n'a pas fonctionné")
        print(f"🔍 Vérification nécessaire de la configuration")















