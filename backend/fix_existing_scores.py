#!/usr/bin/env python3
"""
Script pour corriger les scores existants dans la base de données
"""

import sqlite3
import os
import json

def fix_existing_scores():
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
                   q.question_text, q.question_type, q.options, q.correct_answer,
                   q.points
            FROM quiz_answers qa
            JOIN questions q ON qa.question_id = q.id
        """)
        
        answers = cursor.fetchall()
        print(f"Trouvé {len(answers)} réponses à vérifier")
        
        updated_count = 0
        total_score_fixes = 0
        
        for answer in answers:
            answer_id, question_id, student_answer, is_correct, points_earned, question_text, question_type, options, correct_answer, question_points = answer
            
            print(f"\nTraitement réponse {answer_id} (question {question_id})")
            print(f"Type: {question_type}")
            print(f"Student answer: '{student_answer}'")
            
            # Déterminer la réponse correcte selon le type
            correct_text = ""
            if question_type == "mcq":
                if isinstance(correct_answer, int) and options:
                    # Si c'est un index numérique
                    options_list = json.loads(options) if isinstance(options, str) else options
                    if 0 <= correct_answer < len(options_list):
                        correct_text = options_list[correct_answer]
                        print(f"  Correct answer (index {correct_answer}): '{correct_text}'")
                    else:
                        correct_text = "Réponse correcte non disponible"
                        print(f"  Index invalide: {correct_answer} >= {len(options_list)}")
                elif isinstance(correct_answer, str):
                    # Si c'est déjà une chaîne
                    correct_text = correct_answer
                    print(f"  Correct answer (directe): '{correct_text}'")
                else:
                    correct_text = "Réponse correcte non disponible"
                    print(f"  Type non géré: {type(correct_answer)}")
                    
            elif question_type == "true_false":
                if isinstance(correct_answer, bool):
                    correct_text = "Vrai" if correct_answer else "Faux"
                elif isinstance(correct_answer, str):
                    correct_text = correct_answer
                else:
                    correct_text = "Réponse correcte non disponible"
                print(f"  Correct answer (V/F): '{correct_text}'")
                
            else:
                # Pour les questions texte
                if isinstance(correct_answer, str):
                    correct_text = correct_answer
                else:
                    correct_text = "Réponse correcte non disponible"
                print(f"  Correct answer (texte): '{correct_text}'")
            
            # Nettoyer la réponse correcte des guillemets et caractères d'échappement
            if isinstance(correct_text, str):
                # Supprimer les guillemets au début et à la fin
                if correct_text.startswith('"') and correct_text.endswith('"'):
                    correct_text = correct_text[1:-1]
                
                # Décoder les caractères d'échappement Unicode
                try:
                    correct_text = correct_text.encode('utf-8').decode('unicode_escape')
                except:
                    pass  # Si ça ne marche pas, on garde la version originale
                
                print(f"  Correct answer (nettoyée): '{correct_text}'")
            
            # Vérifier si la réponse est correcte
            student_clean = str(student_answer).strip().lower()
            correct_clean = str(correct_text).strip().lower()
            should_be_correct = student_clean == correct_clean
            
            print(f"  Student clean: '{student_clean}'")
            print(f"  Correct clean: '{correct_clean}'")
            print(f"  Should be correct: {should_be_correct}")
            print(f"  Currently marked as: {is_correct}")
            
            # Si le score est incorrect, le corriger
            if should_be_correct != is_correct:
                new_is_correct = should_be_correct
                new_points_earned = question_points if should_be_correct else 0
                
                cursor.execute("""
                    UPDATE quiz_answers 
                    SET is_correct = ?, points_earned = ?, correct_answer = ?
                    WHERE id = ?
                """, (new_is_correct, new_points_earned, correct_text, answer_id))
                
                updated_count += 1
                if should_be_correct:
                    total_score_fixes += question_points
                
                print(f"  ✅ CORRIGÉ: is_correct={new_is_correct}, points_earned={new_points_earned}")
            else:
                print(f"  ✅ Déjà correct")
        
        # Mettre à jour les scores totaux des résultats
        cursor.execute("""
            SELECT DISTINCT result_id FROM quiz_answers WHERE is_correct = 1
        """)
        result_ids = cursor.fetchall()
        
        for (result_id,) in result_ids:
            cursor.execute("""
                SELECT SUM(points_earned) FROM quiz_answers WHERE result_id = ?
            """, (result_id,))
            total_score = cursor.fetchone()[0] or 0
            
            cursor.execute("""
                UPDATE quiz_results SET score = ? WHERE id = ?
            """, (total_score, result_id))
            
            print(f"Résultat {result_id}: score mis à jour à {total_score}")
        
        # Valider les changements
        conn.commit()
        print(f"\n✅ {updated_count} réponses corrigées")
        print(f"✅ {total_score_fixes} points ajoutés au total")
        
        conn.close()
        print("\n✅ Script terminé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

if __name__ == "__main__":
    fix_existing_scores() 