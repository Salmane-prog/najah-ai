#!/usr/bin/env python3
"""
Script pour corriger les tests sans questions
"""

import sqlite3
import os
from datetime import datetime

def fix_empty_tests():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔧 Correction des tests sans questions")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Identifier les tests sans questions
        print("🔍 Identification des tests sans questions...")
        cursor.execute("""
            SELECT t.id, t.title, t.subject, COUNT(q.id) as question_count
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id
            GROUP BY t.id, t.title, t.subject
            ORDER BY t.id
        """)
        
        tests_status = cursor.fetchall()
        print("\n📊 État des tests:")
        for test in tests_status:
            status = "✅" if test[3] > 0 else "❌"
            print(f"  {status} Test {test[0]}: {test[1]} - {test[3]} questions")
        
        # 2. Créer des questions pour les tests vides
        print(f"\n🔧 Création de questions pour les tests vides...")
        
        # Questions par matière
        questions_data = {
            "Test de Grammaire Française Niveau Intermédiaire": [
                {
                    "text": "Quel est le genre du mot 'table' ?",
                    "type": "multiple_choice",
                    "difficulty": 2,
                    "options": '["Masculin", "Féminin", "Neutre", "Variable"]',
                    "correct": "Féminin",
                    "explanation": "Le mot 'table' est féminin en français.",
                    "objective": "Reconnaissance du genre des noms"
                },
                {
                    "text": "Conjuguez le verbe 'être' à la 1ère personne du singulier au présent.",
                    "type": "multiple_choice",
                    "difficulty": 3,
                    "options": '["Je suis", "Je es", "Je être", "Je suis être"]',
                    "correct": "Je suis",
                    "explanation": "À la 1ère personne du singulier, 'être' se conjugue 'je suis'.",
                    "objective": "Conjugaison du verbe être"
                }
            ],
            "Évaluation Mathématiques - Algèbre": [
                {
                    "text": "Résolvez l'équation : 2x + 5 = 13",
                    "type": "multiple_choice",
                    "difficulty": 3,
                    "options": '["x = 3", "x = 4", "x = 5", "x = 6"]',
                    "correct": "x = 4",
                    "explanation": "2x + 5 = 13 → 2x = 8 → x = 4",
                    "objective": "Résolution d'équations du premier degré"
                },
                {
                    "text": "Factorisez : x² - 9",
                    "type": "multiple_choice",
                    "difficulty": 4,
                    "options": '["(x-3)(x+3)", "(x-3)²", "(x+3)²", "(x-9)(x+1)"]',
                    "correct": "(x-3)(x+3)",
                    "explanation": "x² - 9 = x² - 3² = (x-3)(x+3)",
                    "objective": "Factorisation d'identités remarquables"
                }
            ],
            "Histoire - Révolution Française": [
                {
                    "text": "En quelle année a eu lieu la prise de la Bastille ?",
                    "type": "multiple_choice",
                    "difficulty": 2,
                    "options": '["1787", "1788", "1789", "1790"]',
                    "correct": "1789",
                    "explanation": "La prise de la Bastille a eu lieu le 14 juillet 1789.",
                    "objective": "Chronologie de la Révolution française"
                },
                {
                    "text": "Qui était le roi de France en 1789 ?",
                    "type": "multiple_choice",
                    "difficulty": 2,
                    "options": '["Louis XIV", "Louis XV", "Louis XVI", "Louis XVII"]',
                    "correct": "Louis XVI",
                    "explanation": "Louis XVI était roi de France de 1774 à 1792.",
                    "objective": "Personnages de la Révolution française"
                }
            ],
            "Test Mathématiques - Expert (10-12)": [
                {
                    "text": "Calculez la dérivée de f(x) = x³ + 2x² - 5x + 1",
                    "type": "multiple_choice",
                    "difficulty": 5,
                    "options": '["3x² + 4x - 5", "3x² + 2x - 5", "x² + 4x - 5", "3x² + 4x"]',
                    "correct": "3x² + 4x - 5",
                    "explanation": "f'(x) = 3x² + 4x - 5",
                    "objective": "Calcul de dérivées"
                }
            ],
            "Test Français - Expert (10-12)": [
                {
                    "text": "Identifiez la figure de style dans : 'Le soleil noir de la mélancolie'",
                    "type": "multiple_choice",
                    "difficulty": 5,
                    "options": '["Métaphore", "Comparaison", "Hyperbole", "Litote"]',
                    "correct": "Métaphore",
                    "explanation": "C'est une métaphore car le soleil est comparé à la mélancolie sans mot de comparaison.",
                    "objective": "Reconnaissance des figures de style"
                }
            ]
        }
        
        # 3. Ajouter des questions aux tests vides
        for test_id, test_title, test_subject, question_count in tests_status:
            if question_count == 0 and test_title in questions_data:
                print(f"\n📝 Ajout de questions pour le test {test_id}: {test_title}")
                
                for i, question_data in enumerate(questions_data[test_title]):
                    cursor.execute("""
                        INSERT INTO adaptive_questions (
                            test_id, question_text, question_type, difficulty_level,
                            options, correct_answer, explanation, question_order,
                            learning_objective, is_active
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        test_id, question_data["text"], question_data["type"], 
                        question_data["difficulty"], question_data["options"], 
                        question_data["correct"], question_data["explanation"], 
                        i + 1, question_data["objective"], True
                    ))
                    print(f"  ✅ Question {i+1} ajoutée")
        
        # Valider les changements
        conn.commit()
        
        # 4. Vérifier le résultat
        print(f"\n🔍 Vérification finale:")
        cursor.execute("""
            SELECT t.id, t.title, COUNT(q.id) as question_count
            FROM adaptive_tests t
            LEFT JOIN adaptive_questions q ON t.id = q.test_id
            GROUP BY t.id, t.title
            ORDER BY t.id
        """)
        
        final_status = cursor.fetchall()
        for test in final_status:
            status = "✅" if test[2] > 0 else "❌"
            print(f"  {status} Test {test[0]}: {test[1]} - {test[2]} questions")
        
        conn.close()
        print("\n✅ Correction terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_empty_tests()















