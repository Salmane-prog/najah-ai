#!/usr/bin/env python3
import sqlite3

# Connexion à la base
conn = sqlite3.connect('data/app.db')
cursor = conn.cursor()

print("=== VRAIES DONNÉES DE question_history ===")
cursor.execute('SELECT test_id, question_id, student_response, is_correct FROM question_history LIMIT 5')
rows = cursor.fetchall()

for row in rows:
    print(f"Test {row[0]}, Question {row[1]}, Réponse: '{row[2]}', Correct: {row[3]}")

print("\n=== TESTS RÉCENTS ===")
cursor.execute('''
    SELECT DISTINCT test_id, COUNT(*) as nb_questions 
    FROM question_history 
    GROUP BY test_id 
    ORDER BY test_id DESC 
    LIMIT 5
''')
tests = cursor.fetchall()

for test in tests:
    print(f"Test {test[0]}: {test[1]} questions répondues")

print("\n=== STATUT DES TESTS ===")
cursor.execute('''
    SELECT id, student_id, status, final_score, current_question_index
    FROM french_adaptive_tests 
    ORDER BY id DESC 
    LIMIT 5
''')
tests = cursor.fetchall()

for test in tests:
    print(f"Test {test[0]}: étudiant {test[1]}, statut '{test[2]}', score {test[3]}, question {test[4]}")

conn.close()













