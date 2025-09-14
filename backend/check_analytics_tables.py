import sqlite3

try:
    # Se connecter à la base de données
    conn = sqlite3.connect('data/app.db')
    cursor = conn.cursor()
    
    # Vérifier les tables analytics
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name LIKE 'analytics_%'")
    analytics_tables = cursor.fetchall()
    print("📊 Tables analytics trouvées:")
    for table in analytics_tables:
        print(f"  - {table[0]}")
    
    # Compter les données dans analytics_results
    cursor.execute("SELECT COUNT(*) FROM analytics_results")
    results_count = cursor.fetchone()[0]
    print(f"\n📈 Nombre de résultats analytics: {results_count}")
    
    # Compter les données dans analytics_quizzes
    cursor.execute("SELECT COUNT(*) FROM analytics_quizzes")
    quizzes_count = cursor.fetchone()[0]
    print(f"📊 Nombre de quizzes analytics: {quizzes_count}")
    
    # Afficher quelques exemples
    if results_count > 0:
        cursor.execute("SELECT * FROM analytics_results LIMIT 3")
        print(f"\n🔍 Exemples de résultats:")
        for row in cursor.fetchall():
            print(f"  {row}")
    
    if quizzes_count > 0:
        cursor.execute("SELECT * FROM analytics_quizzes LIMIT 3")
        print(f"\n🔍 Exemples de quizzes:")
        for row in cursor.fetchall():
            print(f"  {row}")
    
    conn.close()
    print("\n✅ Vérification terminée!")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
