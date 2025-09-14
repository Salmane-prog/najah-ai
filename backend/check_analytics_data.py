import sqlite3

try:
    # Se connecter à la base de données
    conn = sqlite3.connect('data/app.db')
    cursor = conn.cursor()
    
    print("🔍 Vérification des données analytics pour l'IA...")
    
    # 1. Vérifier la structure de analytics_results
    cursor.execute("PRAGMA table_info(analytics_results)")
    columns = cursor.fetchall()
    print("\n📋 Structure de analytics_results:")
    for col in columns:
        print(f"  - {col[1]} ({col[2]})")
    
    # 2. Compter les données
    cursor.execute("SELECT COUNT(*) FROM analytics_results")
    total_results = cursor.fetchone()[0]
    print(f"\n📊 Total des résultats: {total_results}")
    
    # 3. Vérifier les scores
    cursor.execute("SELECT MIN(score), MAX(score), AVG(score) FROM analytics_results")
    score_stats = cursor.fetchone()
    print(f"📈 Statistiques des scores: Min={score_stats[0]}, Max={score_stats[1]}, Moy={score_stats[2]:.1f}")
    
    # 4. Vérifier les utilisateurs
    cursor.execute("SELECT DISTINCT user_id FROM analytics_results LIMIT 10")
    user_ids = cursor.fetchall()
    print(f"👥 Utilisateurs avec des résultats: {[uid[0] for uid in user_ids]}")
    
    # 5. Vérifier les dates
    cursor.execute("SELECT MIN(created_at), MAX(created_at) FROM analytics_results")
    date_range = cursor.fetchone()
    print(f"📅 Période des données: {date_range[0]} à {date_range[1]}")
    
    # 6. Exemple de données pour un étudiant
    if user_ids:
        student_id = user_ids[0][0]
        cursor.execute("""
            SELECT score, time_spent, created_at 
            FROM analytics_results 
            WHERE user_id = ? 
            ORDER BY created_at DESC 
            LIMIT 5
        """, (student_id,))
        student_data = cursor.fetchall()
        print(f"\n🔍 Exemple de données pour l'étudiant {student_id}:")
        for row in student_data:
            print(f"  Score: {row[0]}%, Temps: {row[1]}min, Date: {row[2]}")
    
    # 7. Vérifier la table users
    cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
    student_count = cursor.fetchone()[0]
    print(f"\n👨‍🎓 Nombre d'étudiants dans la base: {student_count}")
    
    conn.close()
    print("\n✅ Vérification terminée!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")














