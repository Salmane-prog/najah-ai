#!/usr/bin/env python3
"""
Test des alternatives AI avec prompts personnalisés.
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

def test_local_ai_prompts():
    """Test du service AI local avec prompts personnalisés."""
    print("🤖 Test Local AI avec prompts")
    print("=" * 40)
    
    try:
        from services.local_ai_service import LocalAIService
        
        service = LocalAIService()
        print("✅ Service local initialisé")
        
        # Test 1: Quiz Mathématiques
        print("\n📐 Quiz Mathématiques:")
        quiz_math = service.generate_quiz_question("Mathématiques", "medium", "intermediate")
        print(f"Question: {quiz_math['question']}")
        print(f"Options: {quiz_math['options']}")
        print(f"Réponse: {quiz_math['correct_answer']}")
        
        # Test 2: Quiz Français
        print("\n📚 Quiz Français:")
        quiz_french = service.generate_quiz_question("Français", "easy", "beginner")
        print(f"Question: {quiz_french['question']}")
        print(f"Options: {quiz_french['options']}")
        print(f"Réponse: {quiz_french['correct_answer']}")
        
        # Test 3: Réponse Tuteur
        print("\n👨‍🏫 Réponse Tuteur:")
        tutor_response = service.create_tutor_response(
            {"level": "beginner", "strong_subjects": ["Math"], "weak_subjects": ["Français"]},
            "Comment conjuguer le verbe être au présent?"
        )
        print(f"Réponse: {tutor_response}")
        
        # Test 4: Analyse Réponse
        print("\n📊 Analyse Réponse:")
        analysis = service.analyze_student_response(
            "Je suis, tu es, il est, nous sommes, vous êtes, ils sont",
            "Je suis, tu es, il est, nous sommes, vous êtes, ils sont"
        )
        print(f"Précision: {analysis['precision']}%")
        print(f"Feedback: {analysis['feedback']}")
        print(f"Points forts: {analysis['points_forts']}")
        print(f"Points à améliorer: {analysis['points_amelioration']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_multi_ai_prompts():
    """Test du service Multi-AI avec prompts."""
    print("\n🔄 Test Multi-AI avec prompts")
    print("=" * 40)
    
    try:
        from services.multi_ai_service import MultiAIService
        
        service = MultiAIService()
        print("✅ Service Multi-AI initialisé")
        
        # Afficher les providers
        providers = service.get_available_providers()
        print(f"Providers: {providers}")
        
        # Test 1: Quiz Science
        print("\n🔬 Quiz Science:")
        quiz_science = service.generate_quiz_question("Sciences", "hard", "advanced")
        print(f"Question: {quiz_science['question']}")
        print(f"Généré par: {quiz_science.get('generated_by', 'Inconnu')}")
        
        # Test 2: Tutor Réponse
        print("\n👨‍🏫 Tutor Réponse:")
        tutor_response = service.create_tutor_response(
            {"level": "advanced", "learning_style": "visual"},
            "Expliquez-moi la photosynthèse avec des exemples concrets"
        )
        print(f"Réponse: {tutor_response}")
        
        # Test 3: Analyse Complexe
        print("\n📊 Analyse Complexe:")
        analysis = service.analyze_student_response(
            "La photosynthèse est un processus par lequel les plantes convertissent la lumière solaire en énergie chimique pour produire du glucose et de l'oxygène à partir du dioxyde de carbone et de l'eau.",
            "La photosynthèse est le processus par lequel les plantes utilisent la lumière solaire pour convertir le CO2 et l'eau en glucose et oxygène."
        )
        print(f"Précision: {analysis['precision']}%")
        print(f"Feedback: {analysis['feedback']}")
        print(f"Analysé par: {analysis.get('analyzed_by', 'Inconnu')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_custom_prompts():
    """Test avec des prompts personnalisés."""
    print("\n🎯 Test Prompts Personnalisés")
    print("=" * 40)
    
    try:
        from services.local_ai_service import LocalAIService
        
        service = LocalAIService()
        
        # Prompts personnalisés
        prompts = [
            {
                "topic": "Histoire",
                "difficulty": "medium",
                "level": "intermediate",
                "description": "Quiz sur la Révolution française"
            },
            {
                "topic": "Géographie",
                "difficulty": "easy",
                "level": "beginner",
                "description": "Quiz sur les capitales européennes"
            },
            {
                "topic": "Physique",
                "difficulty": "hard",
                "level": "advanced",
                "description": "Quiz sur la mécanique quantique"
            }
        ]
        
        for i, prompt in enumerate(prompts, 1):
            print(f"\n📝 Prompt {i}: {prompt['description']}")
            print(f"Topic: {prompt['topic']}, Difficulté: {prompt['difficulty']}, Niveau: {prompt['level']}")
            
            quiz = service.generate_quiz_question(
                prompt['topic'],
                prompt['difficulty'],
                prompt['level']
            )
            
            print(f"Question: {quiz['question']}")
            print(f"Options: {quiz['options']}")
            print(f"Réponse: {quiz['correct_answer']}")
            print(f"Explication: {quiz['explanation']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_tutor_scenarios():
    """Test de scénarios de tuteur."""
    print("\n👨‍🏫 Test Scénarios Tuteur")
    print("=" * 40)
    
    try:
        from services.local_ai_service import LocalAIService
        
        service = LocalAIService()
        
        # Scénarios d'étudiants
        scenarios = [
            {
                "student": {"level": "beginner", "weak_subjects": ["Math"]},
                "question": "Je ne comprends pas les fractions, pouvez-vous m'aider?"
            },
            {
                "student": {"level": "intermediate", "strong_subjects": ["Français"]},
                "question": "Comment analyser un texte littéraire?"
            },
            {
                "student": {"level": "advanced", "learning_style": "visual"},
                "question": "Pouvez-vous m'expliquer la théorie de la relativité?"
            }
        ]
        
        for i, scenario in enumerate(scenarios, 1):
            print(f"\n🎓 Scénario {i}:")
            print(f"Étudiant: Niveau {scenario['student']['level']}")
            print(f"Question: {scenario['question']}")
            
            response = service.create_tutor_response(
                scenario['student'],
                scenario['question']
            )
            
            print(f"Réponse Tuteur: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Test principal."""
    print("🚀 Test des Alternatives AI avec Prompts")
    print("=" * 50)
    
    tests = [
        ("Local AI Prompts", test_local_ai_prompts),
        ("Multi-AI Prompts", test_multi_ai_prompts),
        ("Prompts Personnalisés", test_custom_prompts),
        ("Scénarios Tuteur", test_tutor_scenarios)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ Erreur dans {test_name}: {e}")
            results[test_name] = False
    
    print("\n📊 Résultats Finaux:")
    print("=" * 30)
    
    for test_name, success in results.items():
        status = "✅ Réussi" if success else "❌ Échoué"
        print(f"{test_name}: {status}")
    
    success_count = sum(results.values())
    total_count = len(results)
    
    print(f"\n🎯 Résumé: {success_count}/{total_count} tests réussis")
    
    if success_count == total_count:
        print("🎉 Tous les tests sont réussis!")
    elif success_count > 0:
        print("✅ Certains tests fonctionnent")
    else:
        print("❌ Aucun test ne fonctionne")

if __name__ == "__main__":
    main() 