#!/usr/bin/env python3
"""
Script pour vérifier les tables nécessaires à la Phase 2
"""
import sqlite3
import os

def check_phase2_tables():
    """Vérifier les tables nécessaires à la Phase 2"""
    db_path = "F:/IMT/stage/Yancode/Najah__AI/data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 Vérification des tables Phase 2...")
    print("=" * 50)
    
    # Tables principales à vérifier
    tables_to_check = [
        "users",
        "quiz_results", 
        "learning_history",
        "competencies",
        "student_competencies",
        "continuous_assessments",
        "student_continuous_assessments",
        "progress_reports",
        "user_activities",
        "resource_ratings",
        "remediation_plans",
        "remediation_activities",
        "score_corrections",
        "threads",
        "messages",
        "notes",
        "notifications",
        "reports",
        "categories",
        "quiz_assignments",
        "questions",
        "quiz_answers",
        "real_time_activities",
        "class_analytics",
        "student_analytics",
        "learning_path_steps"
    ]
    
    missing_tables = []
    existing_tables = []
    
    for table in tables_to_check:
        try:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                # Vérifier les colonnes
                cursor.execute(f"PRAGMA table_info({table})")
                columns = cursor.fetchall()
                existing_tables.append({
                    'name': table,
                    'columns': [col[1] for col in columns]
                })
                print(f"✅ {table}: {len(columns)} colonnes")
            else:
                missing_tables.append(table)
                print(f"❌ {table}: TABLE MANQUANTE")
        except Exception as e:
            print(f"❌ Erreur vérification {table}: {e}")
    
    print("\n" + "=" * 50)
    print("📊 RÉSUMÉ:")
    print(f"✅ Tables existantes: {len(existing_tables)}")
    print(f"❌ Tables manquantes: {len(missing_tables)}")
    
    if missing_tables:
        print("\n❌ TABLES MANQUANTES:")
        for table in missing_tables:
            print(f"   • {table}")
    
    # Vérifier les colonnes spécifiques qui causent des erreurs
    print("\n🔍 VÉRIFICATION DES COLONNES PROBLÉMATIQUES:")
    
    # Vérifier LearningHistory.created_at
    try:
        cursor.execute("PRAGMA table_info(learning_history)")
        learning_history_columns = [col[1] for col in cursor.fetchall()]
        if 'created_at' in learning_history_columns:
            print("✅ learning_history.created_at: OK")
        else:
            print("❌ learning_history.created_at: MANQUANT")
    except:
        print("❌ Table learning_history: N'EXISTE PAS")
    
    # Vérifier QuizResult.completed
    try:
        cursor.execute("PRAGMA table_info(quiz_results)")
        quiz_results_columns = [col[1] for col in cursor.fetchall()]
        if 'completed' in quiz_results_columns:
            print("✅ quiz_results.completed: OK")
        else:
            print("❌ quiz_results.completed: MANQUANT")
    except:
        print("❌ Table quiz_results: N'EXISTE PAS")
    
    # Vérifier les données de test
    print("\n📊 DONNÉES DE TEST:")
    try:
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='teacher'")
        teacher_count = cursor.fetchone()[0]
        print(f"👨‍🏫 Enseignants: {teacher_count}")
        
        cursor.execute("SELECT COUNT(*) FROM users WHERE role='student'")
        student_count = cursor.fetchone()[0]
        print(f"👨‍🎓 Étudiants: {student_count}")
        
        cursor.execute("SELECT COUNT(*) FROM quiz_results")
        quiz_results_count = cursor.fetchone()[0]
        print(f"📝 Résultats quiz: {quiz_results_count}")
        
        cursor.execute("SELECT COUNT(*) FROM learning_history")
        learning_history_count = cursor.fetchone()[0]
        print(f"📚 Historique apprentissage: {learning_history_count}")
        
    except Exception as e:
        print(f"❌ Erreur vérification données: {e}")
    
    conn.close()

if __name__ == "__main__":
    check_phase2_tables() 