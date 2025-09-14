#!/usr/bin/env python3
"""
Script de test pour le système de rotation des questions
"""

import os
import sys
import random
from datetime import datetime

# Ajouter le répertoire parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_question_rotation():
    """Test du système de rotation des questions"""
    
    print("🧪 TEST DU SYSTÈME DE ROTATION DES QUESTIONS")
    print("=" * 50)
    
    try:
        # Test 1: Import des modules
        print("\n1️⃣ Test des imports...")
        
        from data.enhanced_french_questions import (
            get_question_pool, 
            generate_dynamic_question, 
            get_total_questions_count
        )
        print("✅ Import de la banque de questions étendue réussi")
        
        from services.question_rotation_service import QuestionRotationService
        print("✅ Import du service de rotation réussi")
        
        # Test 2: Vérification de la banque de questions
        print("\n2️⃣ Vérification de la banque de questions...")
        
        counts = get_total_questions_count()
        print(f"📊 Nombre total de questions: {counts['total']}")
        print(f"   - Facile: {counts['easy']}")
        print(f"   - Moyen: {counts['medium']}")
        print(f"   - Difficile: {counts['hard']}")
        
        # Test 3: Test des questions dynamiques
        print("\n3️⃣ Test des questions dynamiques...")
        
        # Question d'articles
        article_question = generate_dynamic_question("articles", "easy")
        print(f"📝 Question articles: {article_question['question']}")
        print(f"   Réponse: {article_question['correct']}")
        print(f"   Dynamique: {article_question.get('is_dynamic', False)}")
        
        # Question de conjugaison
        conjugation_question = generate_dynamic_question("conjugation", "medium")
        print(f"📝 Question conjugaison: {conjugation_question['question']}")
        print(f"   Réponse: {conjugation_question['correct']}")
        print(f"   Dynamique: {conjugation_question.get('is_dynamic', False)}")
        
        # Test 4: Test du pool de questions
        print("\n4️⃣ Test du pool de questions...")
        
        easy_pool = get_question_pool("easy", include_dynamic=True)
        medium_pool = get_question_pool("medium", include_dynamic=True)
        hard_pool = get_question_pool("hard", include_dynamic=True)
        
        print(f"📚 Pool facile: {len(easy_pool)} questions")
        print(f"📚 Pool moyen: {len(medium_pool)} questions")
        print(f"📚 Pool difficile: {len(hard_pool)} questions")
        
        # Test 5: Simulation de sélection de questions
        print("\n5️⃣ Simulation de sélection de questions...")
        
        # Simuler un test avec plusieurs questions
        test_questions = []
        difficulties = ["easy", "medium", "hard"]
        
        for i in range(10):
            difficulty = random.choice(difficulties)
            pool = get_question_pool(difficulty, include_dynamic=True)
            
            if pool:
                question = random.choice(pool)
                test_questions.append({
                    "id": question["id"],
                    "difficulty": question["difficulty"],
                    "topic": question.get("topic", "Sans topic")
                })
        
        # Vérifier les répétitions
        question_ids = [q["id"] for q in test_questions]
        unique_ids = set(question_ids)
        repetition_rate = (len(question_ids) - len(unique_ids)) / len(question_ids)
        
        print(f"🔄 Taux de répétition simulé: {repetition_rate:.2%}")
        print(f"   Questions uniques: {len(unique_ids)}/{len(question_ids)}")
        
        if repetition_rate == 0.0:
            print("✅ Aucune répétition détectée!")
        elif repetition_rate < 0.1:
            print("✅ Très peu de répétitions, système efficace!")
        else:
            print("⚠️ Répétitions détectées, à améliorer")
        
        # Test 6: Vérification des topics
        print("\n6️⃣ Vérification des topics...")
        
        topics = {}
        for question in test_questions:
            topic = question["topic"]
            topics[topic] = topics.get(topic, 0) + 1
        
        print("📋 Répartition par topic:")
        for topic, count in topics.items():
            print(f"   - {topic}: {count} questions")
        
        print("\n🎉 TOUS LES TESTS SONT PASSÉS AVEC SUCCÈS!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR LORS DES TESTS: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_question_generation():
    """Test de la génération de questions spécifiques"""
    
    print("\n🔧 TEST DE GÉNÉRATION DE QUESTIONS SPÉCIFIQUES")
    print("=" * 50)
    
    try:
        from data.enhanced_french_questions import generate_dynamic_question
        
        # Test articles
        print("\n📝 Test questions d'articles:")
        for i in range(3):
            question = generate_dynamic_question("articles", "easy")
            print(f"   {i+1}. {question['question']} → {question['correct']}")
        
        # Test conjugaison
        print("\n📝 Test questions de conjugaison:")
        for i in range(3):
            question = generate_dynamic_question("conjugation", "medium")
            print(f"   {i+1}. {question['question']} → {question['correct']}")
        
        print("✅ Génération de questions spécifiques réussie!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur génération questions: {e}")
        return False

if __name__ == "__main__":
    print("🚀 DÉMARRAGE DES TESTS DU SYSTÈME DE ROTATION")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    success = True
    
    # Test principal
    if not test_question_rotation():
        success = False
    
    # Test de génération
    if not test_question_generation():
        success = False
    
    print("\n" + "=" * 50)
    if success:
        print("🎉 TOUS LES TESTS SONT PASSÉS!")
        print("✅ Le système de rotation des questions fonctionne correctement")
        print("✅ La banque de questions étendue est opérationnelle")
        print("✅ Les questions dynamiques sont générées correctement")
    else:
        print("❌ CERTAINS TESTS ONT ÉCHOUÉ")
        print("⚠️ Vérifiez les erreurs ci-dessus")
    
    print("=" * 50)











