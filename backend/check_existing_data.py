#!/usr/bin/env python3
import sqlite3
import os

def check_database():
    """Vérifier les données existantes dans la base de données"""
    
    # Vérifier le fichier de base de données
    db_path = 'data/app.db'
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"✅ Base de données trouvée: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Vérifier les tables existantes
        print("\n📋 TABLES EXISTANTES:")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"  - {table[0]}")
        
        # 2. Vérifier les questions existantes
        print("\n🔍 QUESTIONS EXISTANTES:")
        try:
            cursor.execute("SELECT COUNT(*) FROM adaptive_questions")
            count = cursor.fetchone()[0]
            print(f"  - Questions adaptatives: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, question_text, subject, difficulty_level FROM adaptive_questions LIMIT 5")
                questions = cursor.fetchall()
                for q in questions:
                    print(f"    * ID {q[0]}: {q[1][:50]}... (Niveau {q[2]})")
        except sqlite3.OperationalError:
            print("  - Table 'adaptive_questions' non trouvée")
        
        # 3. Vérifier les tests existants
        print("\n📝 TESTS EXISTANTS:")
        try:
            cursor.execute("SELECT COUNT(*) FROM adaptive_tests")
            count = cursor.fetchone()[0]
            print(f"  - Tests adaptatifs: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, title, subject, total_questions FROM adaptive_tests LIMIT 5")
                tests = cursor.fetchall()
                for t in tests:
                    print(f"    * ID {t[0]}: {t[1]} ({t[2]}) - {t[3]} questions")
        except sqlite3.OperationalError:
            print("  - Table 'adaptive_tests' non trouvée")
        
        # 4. Vérifier les questions normales
        print("\n❓ QUESTIONS NORMALES:")
        try:
            cursor.execute("SELECT COUNT(*) FROM questions")
            count = cursor.fetchone()[0]
            print(f"  - Questions normales: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, question_text, subject, difficulty FROM questions LIMIT 5")
                questions = cursor.fetchall()
                for q in questions:
                    print(f"    * ID {q[0]}: {q[1][:50]}... (Niveau {q[3]})")
        except sqlite3.OperationalError:
            print("  - Table 'questions' non trouvée")
        
        # 5. Vérifier les quiz normaux
        print("\n📊 QUIZ NORMAUX:")
        try:
            cursor.execute("SELECT COUNT(*) FROM quizzes")
            count = cursor.fetchone()[0]
            print(f"  - Quiz normaux: {count}")
            
            if count > 0:
                cursor.execute("SELECT id, title, subject, total_questions FROM quizzes LIMIT 5")
                quizzes = cursor.fetchall()
                for q in quizzes:
                    print(f"    * ID {q[0]}: {q[1]} ({q[2]}) - {q[3]} questions")
        except sqlite3.OperationalError:
            print("  - Table 'quizzes' non trouvée")
        
        conn.close()
        print("\n✅ Vérification terminée")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")

if __name__ == "__main__":
    check_database()








