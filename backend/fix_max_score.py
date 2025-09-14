#!/usr/bin/env python3
"""
Script pour corriger les max_score manquants dans la base de données
"""

import sqlite3
import os

def fix_max_scores():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    
    print(f"Connexion à la base de données: {db_path}")
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Récupérer tous les résultats de quiz
        cursor.execute("""
            SELECT qr.id, qr.quiz_id, qr.score, qr.max_score,
                   q.total_points
            FROM quiz_results qr
            JOIN quizzes q ON qr.quiz_id = q.id
        """)
        
        results = cursor.fetchall()
        print(f"Trouvé {len(results)} résultats à vérifier")
        
        updated_count = 0
        
        for result in results:
            result_id, quiz_id, score, max_score, total_points = result
            
            print(f"\nRésultat {result_id} (quiz {quiz_id}):")
            print(f"  Score actuel: {score}")
            print(f"  Max score actuel: {max_score}")
            print(f"  Total points du quiz: {total_points}")
            
            # Si max_score est NULL ou 0, le corriger
            if max_score is None or max_score == 0:
                new_max_score = total_points
                cursor.execute("""
                    UPDATE quiz_results 
                    SET max_score = ?
                    WHERE id = ?
                """, (new_max_score, result_id))
                
                updated_count += 1
                print(f"  ✅ CORRIGÉ: max_score mis à {new_max_score}")
            else:
                print(f"  ✅ Déjà correct")
        
        # Valider les changements
        conn.commit()
        print(f"\n✅ {updated_count} résultats corrigés")
        
        conn.close()
        print("\n✅ Script terminé avec succès")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
    
    return True

if __name__ == "__main__":
    fix_max_scores() 