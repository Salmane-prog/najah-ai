#!/usr/bin/env python3
"""
Script Python pour tester et vérifier la base de données Najah AI
"""

import sqlite3
import json
from pathlib import Path
from datetime import datetime

def test_database():
    """Tester et vérifier la base de données"""
    
    db_path = Path("data/app.db")
    
    if not db_path.exists():
        print("❌ Base de données non trouvée. Exécutez d'abord create_database.py")
        return
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("🔍 Test de la base de données Najah AI...")
    print("=" * 50)
    
    # =====================================================
    # 1. VÉRIFIER LES TABLES
    # =====================================================
    
    print("\n📊 1. Vérification des tables...")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
    tables = cursor.fetchall()
    
    expected_tables = [
        'users', 'categories', 'class_groups', 'class_students',
        'quizzes', 'questions', 'quiz_results', 'quiz_answers', 'quiz_assignments',
        'assessments', 'assessment_questions', 'assessment_results',
        'contents', 'learning_paths', 'learning_path_contents', 'learning_history',
        'threads', 'messages', 'notes',
        'badges', 'user_badges', 'user_levels',
        'challenges', 'user_challenges',
        'leaderboards', 'leaderboard_entries',
        'achievements', 'user_achievements'
    ]
    
    found_tables = [table[0] for table in tables]
    missing_tables = set(expected_tables) - set(found_tables)
    
    print(f"✅ Tables trouvées : {len(found_tables)}")
    print(f"📋 Tables attendues : {len(expected_tables)}")
    
    if missing_tables:
        print(f"❌ Tables manquantes : {missing_tables}")
    else:
        print("✅ Toutes les tables sont présentes !")
    
    # =====================================================
    # 2. VÉRIFIER LES DONNÉES
    # =====================================================
    
    print("\n📈 2. Vérification des données...")
    
    # Compter les enregistrements dans chaque table
    table_counts = {}
    for table in found_tables:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            table_counts[table] = count
        except Exception as e:
            print(f"⚠️ Erreur lors du comptage de {table}: {e}")
    
    print("📊 Nombre d'enregistrements par table :")
    for table, count in sorted(table_counts.items()):
        print(f"   {table}: {count}")
    
    # =====================================================
    # 3. VÉRIFIER LES UTILISATEURS
    # =====================================================
    
    print("\n👥 3. Vérification des utilisateurs...")
    
    cursor.execute("""
        SELECT username, role, first_name, last_name 
        FROM users 
        ORDER BY role, username
    """)
    users = cursor.fetchall()
    
    print("👤 Utilisateurs créés :")
    for user in users:
        print(f"   {user[0]} ({user[1]}) - {user[2]} {user[3]}")
    
    # =====================================================
    # 4. VÉRIFIER LES NIVEAUX
    # =====================================================
    
    print("\n📈 4. Vérification des niveaux utilisateurs...")
    
    cursor.execute("""
        SELECT u.username, ul.level, ul.current_xp, ul.total_xp
        FROM users u
        JOIN user_levels ul ON u.id = ul.user_id
        ORDER BY ul.total_xp DESC
    """)
    levels = cursor.fetchall()
    
    print("🏆 Niveaux des utilisateurs :")
    for level in levels:
        print(f"   {level[0]}: Niveau {level[1]} (XP: {level[2]}/{level[3]})")
    
    # =====================================================
    # 5. VÉRIFIER LES QUIZ
    # =====================================================
    
    print("\n📝 5. Vérification des quiz...")
    
    cursor.execute("""
        SELECT title, subject, level, total_points
        FROM quizzes
        ORDER BY subject, level
    """)
    quizzes = cursor.fetchall()
    
    print("📋 Quiz créés :")
    for quiz in quizzes:
        print(f"   {quiz[0]} ({quiz[1]} - {quiz[2]}) - {quiz[3]} points")
    
    # =====================================================
    # 6. VÉRIFIER LES RÉSULTATS
    # =====================================================
    
    print("\n📊 6. Vérification des résultats de quiz...")
    
    cursor.execute("""
        SELECT u.username, qr.sujet, qr.score, qr.max_score, qr.percentage
        FROM quiz_results qr
        JOIN users u ON qr.user_id = u.id
        ORDER BY qr.percentage DESC
    """)
    results = cursor.fetchall()
    
    print("🎯 Résultats de quiz :")
    for result in results:
        print(f"   {result[0]}: {result[1]} - {result[2]}/{result[3]} ({result[4]}%)")
    
    # =====================================================
    # 7. VÉRIFIER LES BADGES
    # =====================================================
    
    print("\n🏆 7. Vérification des badges...")
    
    cursor.execute("""
        SELECT u.username, b.name, ub.progression
        FROM user_badges ub
        JOIN users u ON ub.user_id = u.id
        JOIN badges b ON ub.badge_id = b.id
        ORDER BY u.username, b.name
    """)
    badges = cursor.fetchall()
    
    print("🏅 Badges attribués :")
    for badge in badges:
        status = "✅ Débloqué" if badge[2] >= 1.0 else f"🔄 {badge[2]*100:.0f}%"
        print(f"   {badge[0]}: {badge[1]} - {status}")
    
    # =====================================================
    # 8. VÉRIFIER LES CLASSEMENTS
    # =====================================================
    
    print("\n🏆 8. Vérification des classements...")
    
    cursor.execute("""
        SELECT l.title, u.username, le.score, le.rank
        FROM leaderboard_entries le
        JOIN leaderboards l ON le.leaderboard_id = l.id
        JOIN users u ON le.user_id = u.id
        ORDER BY l.title, le.rank
    """)
    leaderboards = cursor.fetchall()
    
    print("📊 Classements :")
    current_leaderboard = None
    for entry in leaderboards:
        if entry[0] != current_leaderboard:
            current_leaderboard = entry[0]
            print(f"   {current_leaderboard}:")
        print(f"     #{entry[3]} {entry[1]} - {entry[2]} points")
    
    # =====================================================
    # 9. VÉRIFIER LES MESSAGES
    # =====================================================
    
    print("\n💬 9. Vérification des messages...")
    
    cursor.execute("""
        SELECT t.title, u.username, m.content
        FROM messages m
        JOIN threads t ON m.thread_id = t.id
        JOIN users u ON m.user_id = u.id
        ORDER BY t.title, m.created_at
        LIMIT 5
    """)
    messages = cursor.fetchall()
    
    print("💬 Messages récents :")
    for msg in messages:
        print(f"   [{msg[0]}] {msg[1]}: {msg[2][:50]}...")
    
    # =====================================================
    # 10. VÉRIFIER LES CONTENUS
    # =====================================================
    
    print("\n📖 10. Vérification des contenus...")
    
    cursor.execute("""
        SELECT title, subject, level, difficulty, estimated_time
        FROM contents
        ORDER BY subject, level
    """)
    contents = cursor.fetchall()
    
    print("📚 Contenus créés :")
    for content in contents:
        print(f"   {content[0]} ({content[1]} - {content[2]}) - Difficulté: {content[3]}/10 - {content[4]}min")
    
    # =====================================================
    # 11. VÉRIFIER LES PARCOURS
    # =====================================================
    
    print("\n🗺️ 11. Vérification des parcours...")
    
    cursor.execute("""
        SELECT title, subject, level, difficulty, estimated_duration
        FROM learning_paths
        ORDER BY subject, level
    """)
    paths = cursor.fetchall()
    
    print("🛤️ Parcours créés :")
    for path in paths:
        hours = path[4] // 60 if path[4] else 0
        minutes = path[4] % 60 if path[4] else 0
        print(f"   {path[0]} ({path[1]} - {path[2]}) - {path[3]} - {hours}h{minutes}min")
    
    # =====================================================
    # 12. VÉRIFIER LES INDEX
    # =====================================================
    
    print("\n🔍 12. Vérification des index...")
    
    cursor.execute("SELECT name FROM sqlite_master WHERE type='index' AND name NOT LIKE 'sqlite_%'")
    indexes = cursor.fetchall()
    
    print(f"🔍 Index créés : {len(indexes)}")
    for index in indexes:
        print(f"   {index[0]}")
    
    # =====================================================
    # 13. VÉRIFIER LES CONTRAINTES
    # =====================================================
    
    print("\n🔒 13. Vérification des contraintes...")
    
    cursor.execute("PRAGMA foreign_key_list(users)")
    foreign_keys = cursor.fetchall()
    
    print(f"🔗 Clés étrangères trouvées : {len(foreign_keys)}")
    
    # =====================================================
    # 14. TEST DE PERFORMANCE
    # =====================================================
    
    print("\n⚡ 14. Test de performance...")
    
    import time
    
    # Test de requête simple
    start_time = time.time()
    cursor.execute("SELECT COUNT(*) FROM users")
    count = cursor.fetchone()[0]
    simple_query_time = time.time() - start_time
    
    # Test de requête complexe
    start_time = time.time()
    cursor.execute("""
        SELECT u.username, COUNT(qr.id) as quiz_count, AVG(qr.percentage) as avg_score
        FROM users u
        LEFT JOIN quiz_results qr ON u.id = qr.user_id
        WHERE u.role = 'student'
        GROUP BY u.id, u.username
        ORDER BY avg_score DESC
    """)
    complex_results = cursor.fetchall()
    complex_query_time = time.time() - start_time
    
    print(f"⚡ Requête simple : {simple_query_time:.4f}s")
    print(f"⚡ Requête complexe : {complex_query_time:.4f}s")
    print(f"📊 Résultats de la requête complexe :")
    for result in complex_results:
        avg_score = result[2] if result[2] else 0
        print(f"   {result[0]}: {result[1]} quiz, {avg_score:.1f}% de moyenne")
    
    # =====================================================
    # 15. RÉSUMÉ FINAL
    # =====================================================
    
    print("\n" + "=" * 50)
    print("📋 RÉSUMÉ FINAL")
    print("=" * 50)
    
    total_records = sum(table_counts.values())
    print(f"📊 Total d'enregistrements : {total_records}")
    print(f"📋 Tables créées : {len(found_tables)}")
    print(f"🔍 Index créés : {len(indexes)}")
    print(f"👥 Utilisateurs : {table_counts.get('users', 0)}")
    print(f"📝 Quiz : {table_counts.get('quizzes', 0)}")
    print(f"📊 Résultats : {table_counts.get('quiz_results', 0)}")
    print(f"🏆 Badges : {table_counts.get('badges', 0)}")
    print(f"📖 Contenus : {table_counts.get('contents', 0)}")
    print(f"🗺️ Parcours : {table_counts.get('learning_paths', 0)}")
    print(f"💬 Messages : {table_counts.get('messages', 0)}")
    
    # Vérification de l'intégrité
    if len(found_tables) == len(expected_tables) and total_records > 0:
        print("\n✅ Base de données VALIDE et prête pour le développement !")
        print("🎉 Tous les tests sont passés avec succès !")
    else:
        print("\n⚠️ Base de données INCOMPLÈTE - Vérifiez les erreurs ci-dessus")
    
    conn.close()

if __name__ == "__main__":
    try:
        test_database()
    except Exception as e:
        print(f"❌ Erreur lors du test : {e}")
        import traceback
        traceback.print_exc() 