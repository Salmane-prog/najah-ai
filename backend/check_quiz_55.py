#!/usr/bin/env python3
import sqlite3

def check_quiz_55():
    """Vérifier le quiz 55 et ses résultats"""
    
    try:
        conn = sqlite3.connect('data/app.db')
        cursor = conn.cursor()
        
        print("🔍 VÉRIFICATION DU QUIZ 55")
        print("=" * 50)
        
        # 1. Vérifier le test 55
        print("\n📝 TEST 55:")
        cursor.execute("""
            SELECT id, title, subject, total_questions, created_by, created_at
            FROM adaptive_tests 
            WHERE id = 55
        """)
        
        test = cursor.fetchone()
        if test:
            print(f"  ✅ Test trouvé:")
            print(f"     - ID: {test[0]}")
            print(f"     - Titre: {test[1]}")
            print(f"     - Matière: {test[2]}")
            print(f"     - Questions: {test[3]}")
            print(f"     - Créé par: {test[4]}")
            print(f"     - Créé le: {test[5]}")
        else:
            print("  ❌ Test 55 non trouvé")
            return
        
        # 2. Vérifier la tentative de test
        print("\n📋 TENTATIVE DE TEST:")
        cursor.execute("""
            SELECT id, test_id, student_id, total_score, max_score, status, completed_at
            FROM test_attempts 
            WHERE test_id = 55
            ORDER BY id DESC 
            LIMIT 1
        """)
        
        attempt = cursor.fetchone()
        if attempt:
            print(f"  ✅ Tentative trouvée:")
            print(f"     - ID: {attempt[0]}")
            print(f"     - Test ID: {attempt[1]}")
            print(f"     - Étudiant: {attempt[2]}")
            print(f"     - Score: {attempt[3]}/{attempt[4]}")
            print(f"     - Status: {attempt[5]}")
            print(f"     - Terminé: {attempt[6]}")
        else:
            print("  ❌ Aucune tentative trouvée pour le test 55")
            return
        
        # 3. Vérifier les réponses aux questions
        print("\n❓ RÉPONSES AUX QUESTIONS:")
        cursor.execute("""
            SELECT id, question_id, student_answer, is_correct, score
            FROM question_responses 
            WHERE attempt_id = ?
            ORDER BY question_id
        """, (attempt[0],))
        
        responses = cursor.fetchall()
        if responses:
            print(f"  ✅ {len(responses)} réponses trouvées:")
            total_score = 0
            for resp in responses:
                print(f"     - Question {resp[1]}: '{resp[2]}' (Correct: {resp[3]}, Score: {resp[4]})")
                total_score += resp[4]
            print(f"     - Score total calculé: {total_score}")
            print(f"     - Score en base: {attempt[3]}")
            print(f"     - Correspondance: {'✅' if total_score == attempt[3] else '❌'}")
        else:
            print("  ❌ Aucune réponse trouvée")
        
        # 4. Vérifier les questions du test
        print("\n🔍 QUESTIONS DU TEST:")
        cursor.execute("""
            SELECT id, question_text, correct_answer, difficulty_level
            FROM adaptive_questions 
            WHERE test_id = 55 
            ORDER BY question_order
        """)
        
        questions = cursor.fetchall()
        if questions:
            print(f"  ✅ {len(questions)} questions trouvées:")
            for q in questions:
                print(f"     - ID {q[0]}: {q[1][:50]}... (Correct: {q[2]}, Niveau: {q[3]})")
        else:
            print("  ❌ Aucune question trouvée pour le test 55")
        
        conn.close()
        print("\n✅ Vérification terminée")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_quiz_55()








