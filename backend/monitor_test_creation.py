#!/usr/bin/env python3
"""
Script pour surveiller la création de tests en temps réel
"""

import sqlite3
import os
import time
from datetime import datetime

def monitor_test_creation():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔍 Surveillance de la création de tests en temps réel")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier l'état initial
        print("📊 État initial de la base:")
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
        initial_test_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_questions")
        initial_question_count = cursor.fetchone()[0]
        
        print(f"  Tests: {initial_test_count}")
        print(f"  Questions: {initial_question_count}")
        
        # 2. Dernier test connu
        cursor.execute("SELECT MAX(id) FROM adaptive_tests")
        last_test_id = cursor.fetchone()[0] or 0
        print(f"  Dernier test ID: {last_test_id}")
        
        print(f"\n🎯 Maintenant:")
        print(f"  1. Va sur le frontend")
        print(f"  2. Clique sur 'Créer un test'")
        print(f"  3. Remplis le formulaire et soumets")
        print(f"  4. Reviens ici et appuie sur ENTRÉE")
        
        input("Appuie sur ENTRÉE quand tu as créé le test...")
        
        # 3. Vérifier les changements
        print(f"\n🔍 Vérification après création:")
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
        new_test_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM adaptive_questions")
        new_question_count = cursor.fetchone()[0]
        
        print(f"  Tests: {new_test_count} (était: {initial_test_count})")
        print(f"  Questions: {new_question_count} (était: {initial_question_count})")
        
        if new_test_count > initial_test_count:
            print(f"  ✅ {new_test_count - initial_test_count} nouveau(x) test(s) créé(s)")
        else:
            print(f"  ❌ AUCUN nouveau test créé !")
        
        if new_question_count > initial_question_count:
            print(f"  ✅ {new_question_count - initial_question_count} nouvelle(s) question(s) créée(s)")
        else:
            print(f"  ❌ AUCUNE nouvelle question créée !")
        
        # 4. Vérifier le dernier test
        cursor.execute("SELECT MAX(id) FROM adaptive_tests")
        new_last_test_id = cursor.fetchone()[0] or 0
        
        if new_last_test_id > last_test_id:
            print(f"\n🔍 Nouveau test trouvé (ID: {new_last_test_id}):")
            
            cursor.execute("""
                SELECT id, title, is_active, created_at, created_by
                FROM adaptive_tests 
                WHERE id = ?
            """, (new_last_test_id,))
            
            new_test = cursor.fetchone()
            if new_test:
                test_id, title, is_active, created_at, created_by = new_test
                status = "✅ ACTIF" if is_active else "❌ INACTIF"
                print(f"  Titre: {title}")
                print(f"  Statut: {status}")
                print(f"  Créé: {created_at}")
                print(f"  Créé par: {created_by}")
                
                # Vérifier les questions
                cursor.execute("""
                    SELECT COUNT(*) FROM adaptive_questions 
                    WHERE test_id = ?
                """, (new_last_test_id,))
                
                question_count = cursor.fetchone()[0]
                print(f"  Questions: {question_count}")
                
                if question_count == 0:
                    print(f"  ❌ PROBLÈME: Le test n'a AUCUNE question !")
                else:
                    print(f"  ✅ Le test a {question_count} question(s)")
                    
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
                        print(f"  ✅ Test trouvé dans l'endpoint: {endpoint_result[2]} questions")
                    else:
                        print(f"  ❌ Test NON trouvé dans l'endpoint !")
        else:
            print(f"\n❌ AUCUN nouveau test créé !")
        
        conn.close()
        print(f"\n✅ Surveillance terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    monitor_test_creation()


















