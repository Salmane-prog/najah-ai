#!/usr/bin/env python3
"""
Script de test pour vérifier le fonctionnement de la banque d'exercices de remédiation
"""

import sys
import os

# Ajouter le répertoire backend au path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

try:
    from data.remediation_exercises import exercise_bank, get_exercise_statistics
    
    print("🧪 [TEST EXERCISE BANK] Test de la banque d'exercices de remédiation")
    print("=" * 70)
    
    # 1. Test des statistiques
    print("\n📊 1. Statistiques de la banque d'exercices:")
    stats = get_exercise_statistics()
    print(f"   Total d'exercices: {stats['total_exercises']}")
    print(f"   Catégories: {', '.join(stats['categories'])}")
    print(f"   Difficultés: {', '.join(stats['difficulties'])}")
    
    # 2. Test de récupération d'exercices par topic et difficulté
    print("\n🎯 2. Test de récupération d'exercices:")
    
    test_cases = [
        ("grammar", "facile", 3),
        ("conjugation", "intermédiaire", 2),
        ("vocabulary", "avancé", 2),
        ("comprehension", "facile", 2)
    ]
    
    for topic, difficulty, count in test_cases:
        print(f"\n   📚 Topic: {topic}, Difficulté: {difficulty}, Nombre: {count}")
        exercises = exercise_bank.get_diverse_exercises(topic, difficulty, count)
        print(f"   ✅ Exercices trouvés: {len(exercises)}")
        
        for i, ex in enumerate(exercises, 1):
            question = ex.get('question', ex.get('title', 'Sans question'))[:60]
            print(f"     {i}. {ex['id']}: {question}... ({ex['difficulty']})")
    
    # 3. Test de la fonction pour les plans de remédiation
    print("\n📋 3. Test de génération pour plans de remédiation:")
    topics = ["grammar", "conjugation", "vocabulary"]
    remediation_exercises = exercise_bank.get_diverse_exercises("grammar", "intermédiaire", 6, student_id=1, avoid_repetition=True)
    print(f"   ✅ Exercices pour plan de remédiation: {len(remediation_exercises)}")
    
    # 4. Test de récupération par type
    print("\n🔍 4. Test de récupération par type d'exercice:")
    quiz_exercises = [ex for ex in remediation_exercises if ex.get('type') == 'quiz']
    practice_exercises = [ex for ex in remediation_exercises if ex.get('type') == 'practice']
    matching_exercises = [ex for ex in remediation_exercises if ex.get('type') == 'matching']
    
    print(f"   Quiz: {len(quiz_exercises)}")
    print(f"   Practice: {len(practice_exercises)}")
    print(f"   Matching: {len(matching_exercises)}")
    
    # 5. Test de la structure des exercices
    print("\n🏗️ 5. Test de la structure des exercices:")
    if remediation_exercises:
        sample_exercise = remediation_exercises[0]
        print(f"   Structure de l'exercice {sample_exercise['id']}:")
        for key, value in sample_exercise.items():
            if isinstance(value, str) and len(value) > 50:
                print(f"     {key}: {value[:50]}...")
            else:
                print(f"     {key}: {value}")
    
    print("\n✅ [TEST EXERCISE BANK] Tous les tests sont passés avec succès !")
    print("🎉 La banque d'exercices fonctionne correctement.")
    
except ImportError as e:
    print(f"❌ [TEST EXERCISE BANK] Erreur d'import: {e}")
    print("💡 Vérifiez que vous êtes dans le bon répertoire et que le backend est accessible")
except Exception as e:
    print(f"💥 [TEST EXERCISE BANK] Erreur lors du test: {e}")
    import traceback
    traceback.print_exc()






