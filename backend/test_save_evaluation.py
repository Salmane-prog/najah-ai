#!/usr/bin/env python3
"""
Script pour tester la sauvegarde complète d'une évaluation formative
"""

import requests
import json

def test_complete_workflow():
    """Teste le workflow complet : connexion + génération + sauvegarde"""
    
    print("🧪 Test du workflow complet : Connexion + Génération + Sauvegarde")
    print("=" * 80)
    
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
        
        # ÉTAPE 2 : Génération avec l'IA
        print("\n🤖 ÉTAPE 2 : Génération avec l'IA...")
        
        headers = {"Authorization": f"Bearer {token}"}
        
        generation_data = {
            "title": "Test Sauvegarde - Évaluation Formative",
            "subject": "Mathématiques",
            "assessment_type": "project",
            "description": "Test de sauvegarde d'évaluation formative générée par l'IA",
            "target_level": "intermediate",
            "duration_minutes": 60,
            "max_students": 30,
            "learning_objectives": ["Compétence 1", "Compétence 2"],
            "custom_requirements": "Test de sauvegarde"
        }
        
        gen_response = requests.post(
            "http://localhost:8000/api/v1/ai-formative-evaluations/generate-evaluation/",
            headers=headers,
            json=generation_data
        )
        
        if gen_response.status_code != 200:
            print(f"❌ Échec de la génération: {gen_response.text}")
            return None
        
        generated_evaluation = gen_response.json().get("evaluation")
        print(f"✅ Génération IA réussie ! Titre: {generated_evaluation['title']}")
        
        # ÉTAPE 3 : Sauvegarde
        print("\n💾 ÉTAPE 3 : Sauvegarde...")
        
        # Préparer les données pour la sauvegarde
        save_data = {
            "title": generated_evaluation["title"],
            "description": generated_evaluation["description"],
            "assessment_type": generated_evaluation["assessment_type"],
            "subject": "Mathématiques",  # Utiliser le sujet du formulaire
            "target_level": "intermediate",  # Utiliser le niveau du formulaire
            "duration_minutes": 60,  # Utiliser la durée du formulaire
            "max_students": 30,  # Utiliser le nombre d'étudiants du formulaire
            "learning_objectives": ["Compétence 1", "Compétence 2"],  # Utiliser les objectifs du formulaire
            "criteria": generated_evaluation["criteria"],
            "rubric": generated_evaluation["rubric"],
            "questions": generated_evaluation["questions"],
            "instructions": generated_evaluation["instructions"],
            "estimated_duration": generated_evaluation["estimated_duration"],
            "difficulty_level": generated_evaluation["difficulty_level"],
            "success_indicators": generated_evaluation["success_indicators"]
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
            print(f"\n🎉 SUCCÈS COMPLET ! Évaluation sauvegardée !")
            print(f"   ID: {saved_evaluation.get('id')}")
            print(f"   Titre: {saved_evaluation.get('title')}")
            print(f"   Créée par: {saved_evaluation.get('teacher_id')}")
            return True
        else:
            print(f"\n❌ ÉCHEC DE LA SAUVEGARDE")
            print(f"   Erreur: {save_response.text}")
            return False
            
    except Exception as e:
        print(f"\n❌ Erreur lors du test: {e}")
        return False

if __name__ == "__main__":
    print("🔐 Test de sauvegarde d'évaluation formative")
    print("=" * 80)
    
    success = test_complete_workflow()
    
    if success:
        print(f"\n✅ WORKFLOW COMPLET RÉUSSI !")
        print(f"   L'erreur 'Sauvegarde' est maintenant résolue !")
        print(f"\n🔧 POUR TESTER LE FRONTEND :")
        print(f"1. Rafraîchis la page")
        print(f"2. Génère une évaluation avec l'IA")
        print(f"3. Clique sur 'Sauvegarder'")
        print(f"4. L'évaluation devrait être sauvegardée ! 🎉")
    else:
        print(f"\n❌ ÉCHEC ! Le workflow n'a pas fonctionné")
        print(f"🔍 Vérification nécessaire de la configuration")















