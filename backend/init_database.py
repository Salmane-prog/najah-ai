import sqlite3
import os
from datetime import datetime, timedelta
import random

def init_database():
    """Initialiser la base de données avec les tables nécessaires pour les analytics"""
    
    # Chemin vers la base de données
    db_path = "data/app.db"
    
    # Créer le dossier data s'il n'existe pas
    os.makedirs("data", exist_ok=True)
    
    print(f"🗄️ Initialisation de la base de données: {db_path}")
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Table analytics_quizzes (tests pour analytics)
        print("📝 Création de la table analytics_quizzes...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics_quizzes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subject TEXT NOT NULL,
            difficulty_level INTEGER CHECK (difficulty_level BETWEEN 1 AND 10),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # 2. Table analytics_results (résultats des tests pour analytics)
        print("📊 Création de la table analytics_results...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS analytics_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            quiz_id INTEGER NOT NULL,
            score REAL NOT NULL CHECK (score >= 0 AND score <= 100),
            time_spent INTEGER, -- en minutes
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (quiz_id) REFERENCES analytics_quizzes (id)
        )
        """)
        
        # 3. Table class_groups (groupes de classe)
        print("👥 Création de la table class_groups...")
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS class_groups (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            class_id INTEGER NOT NULL,
            student_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES users (id)
        )
        """)
        
        # 4. Index pour optimiser les performances
        print("⚡ Création des index...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_results_user_id ON analytics_results(user_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_results_quiz_id ON analytics_results(quiz_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_results_created_at ON analytics_results(created_at)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_quizzes_subject ON analytics_quizzes(subject)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_analytics_quizzes_difficulty ON analytics_quizzes(difficulty_level)")
        
        # Valider les changements
        conn.commit()
        print("✅ Tables créées avec succès !")
        
        # 5. Insérer des données de test pour les analytics
        print("🧪 Insertion de données de test...")
        insert_test_data(cursor)
        
        # Valider les changements
        conn.commit()
        print("✅ Données de test insérées avec succès !")
        
        # 6. Vérifier la structure
        print("\n📋 Structure de la base de données :")
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        for table in tables:
            print(f"  - {table[0]}")
            
        # Fermer la connexion
        conn.close()
        print(f"\n🎉 Base de données initialisée avec succès : {db_path}")
        
    except Exception as e:
        print(f"❌ Erreur lors de l'initialisation : {e}")
        if 'conn' in locals():
            conn.close()

def insert_test_data(cursor):
    """Insérer des données de test pour les analytics"""
    
    # 1. Insérer des tests
    test_quizzes = [
        ("Test de Grammaire Française - Niveau Intermédiaire", "Français", 6),
        ("Évaluation Vocabulaire - Thème Commerce", "Français", 5),
        ("Test de Compréhension Orale - Niveau Avancé", "Français", 8),
        ("Évaluation Expression Écrite - Rédaction", "Français", 7),
        ("Test de Culture Générale - France Moderne", "Histoire", 6),
        ("Quiz Mathématiques - Algèbre", "Mathématiques", 7),
        ("Test Sciences - Biologie Cellulaire", "Sciences", 8),
        ("Évaluation Géographie - Europe", "Géographie", 5),
        ("Test Littérature - Poésie", "Français", 9),
        ("Quiz Philosophie - Éthique", "Philosophie", 8)
    ]
    
    cursor.executemany("""
        INSERT INTO analytics_quizzes (title, subject, difficulty_level)
        VALUES (?, ?, ?)
    """, test_quizzes)
    
    print(f"  ✅ {len(test_quizzes)} tests insérés")
    
    # 2. Insérer des résultats de tests (simuler l'activité des 30 derniers jours)
    quiz_results = []
    
    # Récupérer les IDs des tests et utilisateurs existants
    cursor.execute("SELECT id FROM analytics_quizzes")
    quiz_ids = [row[0] for row in cursor.fetchall()]
    
    cursor.execute("SELECT id FROM users WHERE role = 'student'")
    student_ids = [row[0] for row in cursor.fetchall()]
    
    if not student_ids:
        print("  ⚠️ Aucun étudiant trouvé, création de données simulées")
        # Créer des utilisateurs étudiants simulés
        for i in range(1, 6):
            cursor.execute("""
                INSERT INTO users (first_name, last_name, email, role, password_hash)
                VALUES (?, ?, ?, 'student', 'simulated_hash')
            """, (f"Étudiant{i}", f"Test{i}", f"etudiant{i}@test.com"))
            student_ids.append(cursor.lastrowid)
    
    # Générer des résultats sur les 30 derniers jours
    base_date = datetime.now() - timedelta(days=30)
    
    for day in range(30):
        current_date = base_date + timedelta(days=day)
        
        # Générer 2-5 résultats par jour
        daily_results = random.randint(2, 5)
        
        for _ in range(daily_results):
            student_id = random.choice(student_ids)
            quiz_id = random.choice(quiz_ids)
            score = random.randint(45, 95)  # Scores réalistes
            time_spent = random.randint(15, 60)  # 15-60 minutes
            
            quiz_results.append((
                student_id,
                quiz_id,
                score,
                time_spent,
                current_date.strftime('%Y-%m-%d %H:%M:%S')
            ))
    
    cursor.executemany("""
        INSERT INTO analytics_results (user_id, quiz_id, score, time_spent, created_at)
        VALUES (?, ?, ?, ?, ?)
    """, quiz_results)
    
    print(f"  ✅ {len(quiz_results)} résultats de tests insérés")
    
    # 3. Insérer des groupes de classe
    class_groups = []
    for student_id in student_ids:
        class_groups.append((1, student_id))  # Tous dans la classe 1
    
    cursor.executemany("""
        INSERT INTO class_groups (class_id, student_id)
        VALUES (?, ?)
    """, class_groups)
    
    print(f"  ✅ {len(class_groups)} groupes de classe créés")

if __name__ == "__main__":
    print("🚀 Initialisation de la base de données Najah__AI...")
    init_database()
    print("\n✨ Initialisation terminée !")

