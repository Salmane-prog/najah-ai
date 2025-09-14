#!/usr/bin/env python3
"""Script de vérification directe SQLite de la base de données"""

import sqlite3
from pathlib import Path

def check_database_sqlite():
    """Vérifier l'état de la base de données avec SQLite direct"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Vérification directe SQLite de: {db_path}")
    
    try:
        # Connexion directe SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Lister toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
        tables = [row[0] for row in cursor.fetchall()]
        print(f"📋 Tables disponibles ({len(tables)}): {', '.join(tables[:10])}...")
        
        # 2. Vérifier les tables essentielles
        essential_tables = ['users', 'class_groups', 'quizzes', 'quiz_results', 'learning_history']
        for table in essential_tables:
            if table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ Table {table}: {count} enregistrements")
                except Exception as e:
                    print(f"⚠️ Table {table}: Erreur de comptage - {e}")
            else:
                print(f"❌ Table {table}: MANQUANTE")
        
        # 3. Vérifier l'utilisateur 42
        print("\n🔍 Vérification de l'utilisateur 42...")
        try:
            cursor.execute("SELECT id, username, email, role FROM users WHERE id = 42")
            user = cursor.fetchone()
            if user:
                print(f"✅ Utilisateur 42: {user}")
            else:
                print("❌ Utilisateur 42 non trouvé")
        except Exception as e:
            print(f"❌ Erreur lors de la recherche de l'utilisateur 42: {e}")
        
        # 4. Vérifier les classes
        print("\n🔍 Vérification des classes...")
        try:
            cursor.execute("SELECT COUNT(*) FROM class_groups")
            class_count = cursor.fetchone()[0]
            print(f"✅ Classes: {class_count}")
            
            if class_count > 0:
                cursor.execute("SELECT id, name, description FROM class_groups LIMIT 3")
                classes = cursor.fetchall()
                for cls in classes:
                    print(f"  - ID: {cls[0]}, Nom: {cls[1]}, Description: {cls[2]}")
        except Exception as e:
            print(f"❌ Erreur lors de la vérification des classes: {e}")
        
        # 5. Vérifier les quiz
        print("\n🔍 Vérification des quiz...")
        try:
            cursor.execute("SELECT COUNT(*) FROM quizzes")
            quiz_count = cursor.fetchone()[0]
            print(f"✅ Quiz: {quiz_count}")
            
            if quiz_count > 0:
                cursor.execute("SELECT id, title, subject, difficulty FROM quizzes LIMIT 3")
                quizzes = cursor.fetchall()
                for quiz in quizzes:
                    print(f"  - ID: {quiz[0]}, Titre: {quiz[1]}, Sujet: {quiz[2]}, Difficulté: {quiz[3]}")
        except Exception as e:
            print(f"❌ Erreur lors de la vérification des quiz: {e}")
        
        # 6. Vérifier les relations
        print("\n🔍 Vérification des relations...")
        try:
            cursor.execute("SELECT COUNT(*) FROM class_students")
            student_class_count = cursor.fetchone()[0]
            print(f"✅ Étudiants dans les classes: {student_class_count}")
            
            if student_class_count > 0:
                cursor.execute("""
                    SELECT cs.class_id, cg.name, cs.student_id, u.username 
                    FROM class_students cs 
                    JOIN class_groups cg ON cs.class_id = cg.id 
                    JOIN users u ON cs.student_id = u.id 
                    LIMIT 3
                """)
                relations = cursor.fetchall()
                for rel in relations:
                    print(f"  - Classe {rel[0]} ({rel[1]}) - Étudiant {rel[2]} ({rel[3]})")
        except Exception as e:
            print(f"❌ Erreur lors de la vérification des relations: {e}")
        
        # 7. Vérifier les tables françaises
        print("\n🔍 Vérification des tables françaises...")
        french_tables = ['french_adaptive_tests', 'french_learning_profiles', 'question_history']
        for table in french_tables:
            if table in tables:
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"✅ Table {table}: {count} enregistrements")
                except Exception as e:
                    print(f"⚠️ Table {table}: Erreur de comptage - {e}")
            else:
                print(f"❌ Table {table}: MANQUANTE")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

if __name__ == "__main__":
    check_database_sqlite()











