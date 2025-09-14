#!/usr/bin/env python3
import sqlite3

def check_all_recent():
    """Vérifier tous les tests et tentatives récentes"""
    
    try:
        conn = sqlite3.connect('data/app.db')
        cursor = conn.cursor()
        
        print("🔍 VÉRIFICATION COMPLÈTE RÉCENTE")
        print("=" * 50)
        
        # 1. Vérifier tous les tests adaptatifs (par ordre décroissant)
        print("\n📝 TOUS LES TESTS ADAPTATIFS (par ordre décroissant):")
        cursor.execute("""
            SELECT id, title, subject, total_questions, created_by, created_at
            FROM adaptive_tests 
            ORDER BY id DESC 
            LIMIT 20
        """)
        
        tests = cursor.fetchall()
        if tests:
            print(f"  ✅ {len(tests)} tests trouvés:")
            for test in tests:
                print(f"     - ID {test[0]}: {test[1]} ({test[2]}) - {test[3]} questions, Créé par {test[4]} le {test[5]}")
        else:
            print("  ❌ Aucun test adaptatif trouvé")
        
        # 2. Vérifier toutes les tentatives récentes
        print("\n📋 TOUTES LES TENTATIVES RÉCENTES:")
        cursor.execute("""
            SELECT id, test_id, student_id, total_score, max_score, status, completed_at
            FROM test_attempts 
            ORDER BY id DESC 
            LIMIT 20
        """)
        
        attempts = cursor.fetchall()
        if attempts:
            print(f"  ✅ {len(attempts)} tentatives trouvées:")
            for attempt in attempts:
                print(f"     - ID {attempt[0]}: Test {attempt[1]}, Étudiant {attempt[2]}, Score {attempt[3]}/{attempt[4]}, Status {attempt[5]}, Terminé {attempt[6]}")
        else:
            print("  ❌ Aucune tentative trouvée")
        
        # 3. Vérifier les réponses récentes
        print("\n❓ RÉPONSES RÉCENTES:")
        cursor.execute("""
            SELECT id, attempt_id, question_id, student_answer, is_correct, score
            FROM question_responses 
            ORDER BY id DESC 
            LIMIT 20
        """)
        
        responses = cursor.fetchall()
        if responses:
            print(f"  ✅ {len(responses)} réponses trouvées:")
            for resp in responses:
                print(f"     - ID {resp[0]}: Tentative {resp[1]}, Question {resp[2]}, Réponse '{resp[3]}', Correct {resp[4]}, Score {resp[5]}")
        else:
            print("  ❌ Aucune réponse trouvée")
        
        # 4. Vérifier les questions récentes
        print("\n🔍 QUESTIONS RÉCENTES:")
        cursor.execute("""
            SELECT id, test_id, question_text, correct_answer, difficulty_level
            FROM adaptive_questions 
            ORDER BY id DESC 
            LIMIT 20
        """)
        
        questions = cursor.fetchall()
        if questions:
            print(f"  ✅ {len(questions)} questions trouvées:")
            for q in questions:
                print(f"     - ID {q[0]}: Test {q[1]}, Question: {q[2][:50]}..., Correct: {q[3]}, Niveau: {q[4]}")
        else:
            print("  ❌ Aucune question trouvée")
        
        conn.close()
        print("\n✅ Vérification terminée")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_all_recent()








