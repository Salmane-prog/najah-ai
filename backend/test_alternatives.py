#!/usr/bin/env python3
"""
Test des alternatives AI gratuites.
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_local_ai():
    """Test du service AI local."""
    print("🤖 Test du service AI local")
    print("=" * 40)
    
    try:
        from services.local_ai_service import LocalAIService
        
        service = LocalAIService()
        print("✅ Service local initialisé")
        
        # Test de génération de quiz
        quiz = service.generate_quiz_question("Mathématiques", "medium", "intermediate")
        print("✅ Quiz généré localement!")
        print(f"Question: {quiz['question']}")
        print(f"Options: {quiz['options']}")
        print(f"Réponse correcte: {quiz['correct_answer']}")
        
        # Test de réponse de tuteur
        tutor_response = service.create_tutor_response(
            {"level": "intermediate"}, 
            "Comment résoudre une équation du premier degré?"
        )
        print(f"✅ Réponse tuteur: {tutor_response}")
        
        # Test d'analyse
        analysis = service.analyze_student_response(
            "La réponse est 5", 
            "La réponse est 5"
        )
        print(f"✅ Analyse: {analysis}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur service local: {e}")
        return False

def test_huggingface():
    """Test du service Hugging Face."""
    print("\n🤗 Test du service Hugging Face")
    print("=" * 40)
    
    try:
        from services.huggingface_service import HuggingFaceService
        
        service = HuggingFaceService()
        print("✅ Service Hugging Face initialisé")
        
        # Test de génération de quiz
        quiz = service.generate_quiz_question("Mathématiques", "medium", "intermediate")
        print("✅ Quiz généré avec Hugging Face!")
        print(f"Question: {quiz['question']}")
        print(f"Options: {quiz['options']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Hugging Face: {e}")
        return False

def test_multi_ai():
    """Test du service multi-provider."""
    print("\n🔄 Test du service Multi-AI")
    print("=" * 40)
    
    try:
        from services.multi_ai_service import MultiAIService
        
        service = MultiAIService()
        print("✅ Service Multi-AI initialisé")
        
        # Afficher les providers disponibles
        providers = service.get_available_providers()
        print(f"Providers disponibles: {providers}")
        
        # Test de génération
        quiz = service.generate_quiz_question("Mathématiques", "medium", "intermediate")
        print("✅ Quiz généré avec Multi-AI!")
        print(f"Question: {quiz['question']}")
        print(f"Généré par: {quiz.get('generated_by', 'Inconnu')}")
        
        # Statistiques
        stats = service.get_usage_stats()
        print(f"Statistiques: {stats}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur Multi-AI: {e}")
        return False

def test_all_alternatives():
    """Test toutes les alternatives."""
    print("🚀 Test de toutes les alternatives AI")
    print("=" * 50)
    
    results = {
        "Local AI": test_local_ai(),
        "Hugging Face": test_huggingface(),
        "Multi-AI": test_multi_ai()
    }
    
    print("\n📊 Résultats:")
    print("=" * 30)
    
    for name, success in results.items():
        status = "✅ Fonctionne" if success else "❌ Échec"
        print(f"{name}: {status}")
    
    working_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n🎯 Résumé: {working_count}/{total_count} services fonctionnent")
    
    if working_count > 0:
        print("✅ Vous avez des alternatives AI fonctionnelles!")
    else:
        print("❌ Aucune alternative AI ne fonctionne")

if __name__ == "__main__":
    test_all_alternatives() 