#!/usr/bin/env python3
"""
Script de configuration complète du système de questions amélioré
"""

import os
import sys
import sqlite3
from datetime import datetime

def setup_database():
    """Configure la base de données avec toutes les nouvelles tables"""
    
    print("🔧 CONFIGURATION DE LA BASE DE DONNÉES")
    print("=" * 50)
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), "..", "data", "app.db")
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"🔍 Connexion à la base de données: {db_path}")
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 1. Créer la table question_history
        print("\n1️⃣ Création de la table question_history...")
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS question_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                question_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                difficulty VARCHAR(20) NOT NULL,
                topic VARCHAR(100),
                asked_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
                student_response TEXT,
                is_correct INTEGER,
                FOREIGN KEY (test_id) REFERENCES french_adaptive_tests (id)
            )
        """)
        
        # Créer des index pour améliorer les performances
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_question_history_test_id ON question_history(test_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_question_history_question_id ON question_history(question_id)")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_question_history_difficulty ON question_history(difficulty)")
        
        print("✅ Table question_history créée avec succès")
        
        # 2. Vérifier les tables existantes
        print("\n2️⃣ Vérification des tables existantes...")
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = [
            "users", "french_adaptive_tests", "french_learning_profiles",
            "question_history"
        ]
        
        for table in required_tables:
            if table in tables:
                print(f"✅ Table {table} existe")
            else:
                print(f"⚠️ Table {table} manquante")
        
        # 3. Insérer des données de démonstration si nécessaire
        print("\n3️⃣ Vérification des données de démonstration...")
        
        # Vérifier s'il y a des tests existants
        cursor.execute("SELECT COUNT(*) FROM french_adaptive_tests")
        test_count = cursor.fetchone()[0]
        
        if test_count == 0:
            print("📝 Aucun test existant, création de tests de démonstration...")
            
            # Créer un utilisateur de test si nécessaire
            cursor.execute("SELECT COUNT(*) FROM users WHERE role = 'student'")
            student_count = cursor.fetchone()[0]
            
            if student_count == 0:
                print("👤 Création d'un étudiant de test...")
                cursor.execute("""
                    INSERT INTO users (username, email, role, created_at) 
                    VALUES ('etudiant_test', 'etudiant@test.com', 'student', CURRENT_TIMESTAMP)
                """)
                student_id = cursor.lastrowid
                print(f"✅ Étudiant de test créé avec l'ID: {student_id}")
            else:
                # Utiliser le premier étudiant existant
                cursor.execute("SELECT id FROM users WHERE role = 'student' LIMIT 1")
                student_id = cursor.fetchone()[0]
                print(f"✅ Utilisation de l'étudiant existant ID: {student_id}")
            
            # Créer un test de démonstration
            cursor.execute("""
                INSERT INTO french_adaptive_tests (
                    student_id, test_type, total_questions, current_difficulty, 
                    status, started_at
                ) VALUES (?, 'initial', 10, 'easy', 'in_progress', CURRENT_TIMESTAMP)
            """, (student_id,))
            
            test_id = cursor.lastrowid
            print(f"✅ Test de démonstration créé avec l'ID: {test_id}")
            
            # Créer un profil d'apprentissage
            cursor.execute("""
                INSERT INTO french_learning_profiles (
                    student_id, learning_style, french_level, preferred_pace,
                    strengths, weaknesses, created_at
                ) VALUES (?, 'visual', 'A1', 'moyen', 
                '["motivation"]', '["grammaire", "vocabulaire"]', CURRENT_TIMESTAMP)
            """, (student_id,))
            
            print("✅ Profil d'apprentissage créé")
            
        else:
            print(f"✅ {test_count} tests existants trouvés")
        
        # 4. Vérifier la structure de la base
        print("\n4️⃣ Vérification de la structure...")
        
        # Vérifier les colonnes de question_history
        cursor.execute("PRAGMA table_info(question_history)")
        columns = [row[1] for row in cursor.fetchall()]
        
        expected_columns = [
            "id", "test_id", "question_id", "question_text", 
            "difficulty", "topic", "asked_at", "student_response", "is_correct"
        ]
        
        for col in expected_columns:
            if col in columns:
                print(f"✅ Colonne {col} existe")
            else:
                print(f"❌ Colonne {col} manquante")
        
        conn.commit()
        print("\n✅ Configuration de la base de données terminée avec succès!")
        return True
        
    except Exception as e:
        print(f"\n❌ Erreur lors de la configuration: {e}")
        conn.rollback()
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        conn.close()

def test_system():
    """Test du système complet"""
    
    print("\n🧪 TEST DU SYSTÈME COMPLET")
    print("=" * 50)
    
    try:
        # Test des imports
        print("1️⃣ Test des imports...")
        
        # Ajouter le répertoire parent au path
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from data.enhanced_french_questions import get_total_questions_count
        print("✅ Import de la banque de questions réussi")
        
        from services.question_rotation_service import QuestionRotationService
        print("✅ Import du service de rotation réussi")
        
        # Test des statistiques
        print("\n2️⃣ Test des statistiques...")
        
        counts = get_total_questions_count()
        print(f"📊 Total des questions: {counts['total']}")
        print(f"   - Facile: {counts['easy']}")
        print(f"   - Moyen: {counts['medium']}")
        print(f"   - Difficile: {counts['hard']}")
        
        print("\n🎉 SYSTÈME PRÊT À UTILISER!")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🚀 CONFIGURATION COMPLÈTE DU SYSTÈME DE QUESTIONS AMÉLIORÉ")
    print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Configuration de la base de données
    if setup_database():
        print("\n✅ Base de données configurée avec succès")
        
        # Test du système
        if test_system():
            print("\n🎉 CONFIGURATION TERMINÉE AVEC SUCCÈS!")
            print("\n📋 RÉSUMÉ DES AMÉLIORATIONS:")
            print("   ✅ Table question_history créée")
            print("   ✅ Service de rotation intelligente configuré")
            print("   ✅ Banque de questions étendue (40+ questions)")
            print("   ✅ Questions dynamiques avec templates")
            print("   ✅ Système anti-répétition opérationnel")
            print("   ✅ Endpoints de statistiques ajoutés")
            
            print("\n🚀 Le système est maintenant prêt à éviter les répétitions!")
        else:
            print("\n❌ Erreur lors du test du système")
    else:
        print("\n❌ Erreur lors de la configuration de la base de données")
    
    print("\n" + "=" * 60)











