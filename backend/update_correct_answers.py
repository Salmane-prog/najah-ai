#!/usr/bin/env python3
"""
Script pour mettre à jour les réponses correctes dans la base de données
"""

import sqlite3
import os
import json

def update_correct_answers():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    print(f"Connexion à la base de données: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer toutes les réponses de quiz
        cursor.execute("""
            SELECT qa.id, qa.question_id, qa.student_answer, qa.is_correct, qa.points_earned,
                   q.question_text, q.question_type, q.options, q.correct_answer
            FROM quiz_answers qa
            JOIN questions q ON qa.question_id = q.id
            WHERE qa.correct_answer IS NULL
        """)
        
        answers = cursor.fetchall()
        print(f"Trouvé {len(answers)} réponses à mettre à jour")
        
        updated_count = 0
        
        for answer in answers:
            answer_id, question_id, student_answer, is_correct, points_earned, question_text, question_type, options, correct_answer = answer
            
            print(f"\nTraitement réponse {answer_id} (question {question_id})")
            print(f"Type: {question_type}")
            print(f"Question: {question_text[:50]}...")
            
            # Déterminer la réponse correcte selon le type
            if question_type == "mcq":
                if isinstance(correct_answer, int) and options:
                    # Si c'est un index numérique
                    options_list = json.loads(options) if isinstance(options, str) else options
                    if 0 <= correct_answer < len(options_list):
                        final_correct_answer = options_list[correct_answer]
                        print(f"  Réponse correcte (index {correct_answer}): {final_correct_answer}")
                    else:
                        final_correct_answer = "Réponse correcte non disponible"
                        print(f"  Index invalide: {correct_answer} >= {len(options_list)}")
                elif isinstance(correct_answer, str):
                    # Si c'est déjà une chaîne
                    final_correct_answer = correct_answer
                    print(f"  Réponse correcte (directe): {final_correct_answer}")
                else:
                    final_correct_answer = "Réponse correcte non disponible"
                    print(f"  Type non géré: {type(correct_answer)}")
                    
            elif question_type == "true_false":
                if isinstance(correct_answer, bool):
                    final_correct_answer = "Vrai" if correct_answer else "Faux"
                elif isinstance(correct_answer, str):
                    final_correct_answer = correct_answer
                else:
                    final_correct_answer = "Réponse correcte non disponible"
                print(f"  Réponse correcte (V/F): {final_correct_answer}")
                
            else:
                # Pour les questions texte
                if isinstance(correct_answer, str):
                    final_correct_answer = correct_answer
                else:
                    final_correct_answer = "Réponse correcte non disponible"
                print(f"  Réponse correcte (texte): {final_correct_answer}")
            
            # Mettre à jour la base de données
            cursor.execute("""
                UPDATE quiz_answers 
                SET correct_answer = ? 
                WHERE id = ?
            """, (final_correct_answer, answer_id))
            
            updated_count += 1
        
        # Valider les changements
        conn.commit()
        print(f"\n✅ {updated_count} réponses mises à jour avec succès")
        
        # Vérifier les résultats
        cursor.execute("""
            SELECT COUNT(*) as total,
                   COUNT(CASE WHEN correct_answer IS NOT NULL THEN 1 END) as with_correct_answer
            FROM quiz_answers
        """)
        
        stats = cursor.fetchone()
        print(f"\nStatistiques:")
        print(f"  Total réponses: {stats[0]}")
        print(f"  Avec réponse correcte: {stats[1]}")
        
        conn.close()
        print("\n✅ Script terminé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

if __name__ == "__main__":
    update_correct_answers() 