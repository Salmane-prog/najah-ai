#!/usr/bin/env python3
"""
Script pour tester la sauvegarde dans formative_assessments
"""

import requests
import json

def test_save_formative_assessment():
    """Teste la sauvegarde d'une évaluation formative dans formative_assessments"""
    
    print("🧪 Test de sauvegarde dans formative_assessments")
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
        
        # ÉTAPE 2 : Test direct de sauvegarde
        print("\n💾 ÉTAPE 2 : Test de sauvegarde...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        # Données simplifiées pour formative_assessments
        save_data = {
            "title": "Test Sauvegarde - Évaluation Formative",
            "subject": "Mathématiques",
            "description": "Test de sauvegarde d'évaluation formative dans la table formative_assessments",
            "assessment_type": "project",
            "target_level": "intermediate",
            "duration_minutes": 60,
            "max_students": 30,
            "learning_objectives": ["Compétence 1", "Compétence 2"],
            "custom_requirements": "Test de sauvegarde"
        }
        
        print(f"📊 Données à sauvegarder: {json.dumps(save_data, indent=2)}")
        
        save_response = requests.post(
            "http://localhost:8000/api/v1/formative-evaluations/",
            headers=headers,
            json=save_data
        )
        
        print(f"\n📊 Réponse de sauvegarde:")
        print(f"   Status: {save_response.status_code}")
        print(f"   Headers: {dict(save_response.headers)}")
        print(f"   Body: {save_response.text}")
        
        if save_response.status_code == 200:
            saved_evaluation = save_response.json()
            print(f"\n🎉 SUCCÈS ! Évaluation sauvegardée dans formative_assessments !")
            print(f"   ID: {saved_evaluation.get('id')}")
            print(f"   Titre: {saved_evaluation.get('title')}")
            print(f"   Créée par: {saved_evaluation.get('created_by')}")
            return True
        else:
            print(f"\n❌ ÉCHEC DE LA SAUVEGARDE")
            print(f"   Erreur: {save_response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Test de sauvegarde dans formative_assessments")
    print("=" * 80)
    
    success = test_save_formative_assessment()
    
    if success:
        print(f"\n✅ SAUVEGARDE RÉUSSIE !")
        print(f"   L'erreur 'Sauvegarde' est maintenant résolue !")
        print(f"\n🔧 POUR TESTER LE FRONTEND :")
        print(f"1. Rafraîchis la page")
        print(f"2. Génère une évaluation avec l'IA")
        print(f"3. Clique sur 'Sauvegarder'")
        print(f"4. L'évaluation devrait être sauvegardée ! 🎉")
    else:
        print(f"\n❌ ÉCHEC ! La sauvegarde n'a pas fonctionné")
        print(f"🔍 Vérification nécessaire de la configuration")


















