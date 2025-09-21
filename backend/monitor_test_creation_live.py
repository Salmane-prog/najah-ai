#!/usr/bin/env python3
"""
Script de surveillance en temps réel de la création de tests
"""

import sqlite3
import os
import time
from datetime import datetime

def monitor_test_creation_live():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔍 Surveillance en temps réel de la création de tests")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. État initial
        print("📊 État initial de la base:")
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
        initial_test_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_questions")
        initial_question_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT MAX(id) FROM adaptive_tests")
        last_test_id = cursor.fetchone()[0] or 0
        
        print(f"  Tests: {initial_test_count}")
        print(f"  Questions: {initial_question_count}")
        print(f"  Dernier test ID: {last_test_id}")
        
        print(f"\n🎯 Maintenant:")
        print(f"  1. Va sur le frontend")
        print(f"  2. Clique sur '+ Créer un Test' (bouton vert)")
        print(f"  3. Remplis le formulaire et soumets")
        print(f"  4. Reviens ici et appuie sur ENTRÉE")
        
        input("Appuie sur ENTRÉE quand tu as créé le test...")
        
        # 2. Vérification immédiate
        print(f"\n🔍 Vérification après création:")
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
        new_test_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_questions")
        new_question_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT MAX(id) FROM adaptive_tests")
        new_last_test_id = cursor.fetchone()[0] or 0
        
        print(f"  Tests: {new_test_count} (était: {initial_test_count})")
        print(f"  Questions: {new_question_count} (était: {initial_question_count})")
        print(f"  Dernier test ID: {new_last_test_id} (était: {last_test_id})")
        
        # 3. Analyse des changements
        if new_test_count > initial_test_count:
            print(f"  ✅ {new_test_count - initial_test_count} nouveau(x) test(s) créé(s)")
        else:
            print(f"  ❌ AUCUN nouveau test créé !")
        
        if new_question_count > initial_question_count:
            print(f"  ✅ {new_question_count - initial_question_count} nouvelle(s) question(s) créée(s)")
        else:
            print(f"  ❌ AUCUNE nouvelle question créée !")
        
        if new_last_test_id > last_test_id:
            print(f"  ✅ Nouveau test trouvé avec l'ID: {new_last_test_id}")
            
            # Détails du nouveau test
            cursor.execute("""
                SELECT id, title, is_active, created_at, created_by
                FROM adaptive_tests 
                WHERE id = ?
            """, (new_last_test_id,))
            
            new_test = cursor.fetchone()
            if new_test:
                test_id, title, is_active, created_at, created_by = new_test
                status = "✅ ACTIF" if is_active else "❌ INACTIF"
                print(f"    Titre: {title}")
                print(f"    Statut: {status}")
                print(f"    Créé: {created_at}")
                print(f"    Créé par: {created_by}")
                
                # Vérifier les questions
                cursor.execute("""
                    SELECT COUNT(*) FROM adaptive_questions 
                    WHERE test_id = ?
                """, (new_last_test_id,))
                
                question_count = cursor.fetchone()[0]
                print(f"    Questions: {question_count}")
                
                if question_count == 0:
                    print(f"    ❌ PROBLÈME: Le test n'a AUCUNE question !")
                else:
                    print(f"    ✅ Le test a {question_count} question(s)")
                    
                    # Vérifier l'endpoint
                    cursor.execute("""
                        SELECT 
                            t.id,
                            t.title,
                            COUNT(q.id) as question_count
                        FROM adaptive_tests t
                        LEFT JOIN adaptive_questions q ON t.id = q.test_id AND q.is_active = 1
                        WHERE t.id = ? AND t.is_active = 1
                        GROUP BY t.id
                    """, (new_last_test_id,))
                    
                    endpoint_result = cursor.fetchone()
                    if endpoint_result:
                        print(f"    ✅ Test trouvé dans l'endpoint: {endpoint_result[2]} questions")
                    else:
                        print(f"    ❌ Test NON trouvé dans l'endpoint !")
        else:
            print(f"\n❌ AUCUN nouveau test créé !")
            
            # Vérifier s'il y a des erreurs dans la base
            print(f"\n🔍 Vérification des erreurs possibles:")
            
            # Vérifier les tests récents
            cursor.execute("""
                SELECT id, title, is_active, created_at
                FROM adaptive_tests 
                WHERE created_at > datetime('now', '-5 minutes')
                ORDER BY created_at DESC
            """)
            
            recent_tests = cursor.fetchall()
            if recent_tests:
                print(f"  Tests créés dans les 5 dernières minutes:")
                for test in recent_tests:
                    status = "✅ ACTIF" if test[2] else "❌ INACTIF"
                    print(f"    ID {test[0]}: {test[1]} - {status} - {test[3]}")
            else:
                print(f"  Aucun test créé dans les 5 dernières minutes")
        
        conn.close()
        print(f"\n✅ Surveillance terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    monitor_test_creation_live()


















