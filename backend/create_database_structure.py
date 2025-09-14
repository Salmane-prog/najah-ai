#!/usr/bin/env python3
"""
Script pour créer la structure complète de la base de données
"""

import sqlite3
import os
import hashlib
from datetime import datetime

def create_database_structure():
    """Crée la structure complète de la base de données"""
    
    db_path = "app.db"
    
    print(f"🗄️ Création de la structure de la base de données: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 1. Table users
        print("📋 Création de la table 'users'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                role TEXT NOT NULL CHECK (role IN ('student', 'teacher', 'admin')),
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # 2. Table adaptive_tests
        print("📋 Création de la table 'adaptive_tests'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adaptive_tests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                subject TEXT NOT NULL,
                difficulty_level TEXT NOT NULL CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
                adaptation_type TEXT NOT NULL CHECK (adaptation_type IN ('difficulty', 'content', 'both')),
                total_questions INTEGER DEFAULT 0,
                estimated_duration INTEGER DEFAULT 60,
                is_active BOOLEAN DEFAULT 1,
                created_by INTEGER,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL
            )
        """)
        
        # 3. Table adaptive_questions
        print("📋 Création de la table 'adaptive_questions'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS adaptive_questions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                question_text TEXT NOT NULL,
                question_type TEXT NOT NULL CHECK (question_type IN ('multiple_choice', 'true_false', 'short_answer', 'essay')),
                cognitive_level TEXT NOT NULL CHECK (cognitive_level IN ('remember', 'understand', 'apply', 'analyze', 'evaluate', 'create')),
                difficulty_level TEXT NOT NULL CHECK (difficulty_level IN ('easy', 'medium', 'hard')),
                options TEXT,
                correct_answer TEXT,
                explanation TEXT,
                points INTEGER DEFAULT 1,
                is_active BOOLEAN DEFAULT 1,
                question_order INTEGER DEFAULT 0,
                learning_objective TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # 4. Table test_assignments
        print("📋 Création de la table 'test_assignments'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS test_assignments (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_id INTEGER NOT NULL,
                class_id INTEGER NOT NULL,
                assigned_by INTEGER,
                assigned_at TEXT NOT NULL,
                due_date TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        """)
        
        # 5. Table classes
        print("📋 Création de la table 'classes'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS classes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                subject TEXT NOT NULL,
                teacher_id INTEGER NOT NULL,
                academic_year TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)
        
        # 6. Table students
        print("📋 Création de la table 'students'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                first_name TEXT NOT NULL,
                last_name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                class_id INTEGER NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL
            )
        """)
        
        # 7. Table formative_evaluations
        print("📋 Création de la table 'formative_evaluations'...")
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS formative_evaluations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT NOT NULL,
                assessment_type TEXT NOT NULL,
                subject TEXT NOT NULL,
                target_level TEXT NOT NULL,
                duration_minutes INTEGER NOT NULL,
                max_students INTEGER NOT NULL,
                learning_objectives TEXT NOT NULL,
                criteria TEXT NOT NULL,
                rubric TEXT NOT NULL,
                questions TEXT NOT NULL,
                instructions TEXT NOT NULL,
                estimated_duration INTEGER NOT NULL,
                difficulty_level TEXT NOT NULL,
                success_indicators TEXT NOT NULL,
                is_active BOOLEAN DEFAULT 1,
                created_at TEXT NOT NULL,
                teacher_id INTEGER NOT NULL
            )
        """)
        
        # Valider toutes les créations
        conn.commit()
        print("✅ Structure de la base de données créée avec succès !")
        
        # Vérifier les tables créées
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"\n📋 Tables créées ({len(tables)}):")
        for table in tables:
            print(f"  - {table[0]}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création de la structure: {e}")
        if 'conn' in locals():
            conn.close()
        return False

def create_test_data():
    """Crée des données de test dans la base de données"""
    
    print("\n👤 Création des données de test...")
    
    try:
        conn = sqlite3.connect("app.db")
        cursor = conn.cursor()
        
        # 1. Créer un utilisateur enseignant de test
        print("👨‍🏫 Création de l'utilisateur enseignant de test...")
        
        test_teacher = {
            'email': 'teacher@example.com',
            'password': hashlib.sha256('teacher123'.encode()).hexdigest(),
            'first_name': 'Test',
            'last_name': 'Teacher',
            'role': 'teacher',
            'is_active': True,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        cursor.execute("""
            INSERT OR REPLACE INTO users (email, password, first_name, last_name, role, is_active, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            test_teacher['email'],
            test_teacher['password'],
            test_teacher['first_name'],
            test_teacher['last_name'],
            test_teacher['role'],
            test_teacher['is_active'],
            test_teacher['created_at'],
            test_teacher['updated_at']
        ))
        
        teacher_id = cursor.lastrowid
        print(f"✅ Enseignant créé avec l'ID: {teacher_id}")
        
        # 2. Créer une classe de test
        print("🏫 Création d'une classe de test...")
        
        test_class = {
            'name': 'Classe Test 6ème A',
            'subject': 'Mathématiques',
            'teacher_id': teacher_id,
            'academic_year': '2024-2025',
            'is_active': True,
            'created_at': datetime.now().isoformat()
        }
        
        cursor.execute("""
            INSERT OR REPLACE INTO classes (name, subject, teacher_id, academic_year, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            test_class['name'],
            test_class['subject'],
            test_class['teacher_id'],
            test_class['academic_year'],
            test_class['is_active'],
            test_class['created_at']
        ))
        
        class_id = cursor.lastrowid
        print(f"✅ Classe créée avec l'ID: {class_id}")
        
        # 3. Créer des étudiants de test
        print("👥 Création d'étudiants de test...")
        
        test_students = [
            ('Alice', 'Dupont', 'alice.dupont@test.com'),
            ('Bob', 'Martin', 'bob.martin@test.com'),
            ('Clara', 'Bernard', 'clara.bernard@test.com')
        ]
        
        for first_name, last_name, email in test_students:
            cursor.execute("""
                INSERT OR REPLACE INTO students (first_name, last_name, email, class_id, is_active, created_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                first_name,
                last_name,
                email,
                class_id,
                True,
                datetime.now().isoformat()
            ))
            print(f"✅ Étudiant créé: {first_name} {last_name}")
        
        # Valider toutes les insertions
        conn.commit()
        print("✅ Données de test créées avec succès !")
        
        # Vérifier les données créées
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM classes")
        class_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM students")
        student_count = cursor.fetchone()[0]
        
        print(f"\n📊 Résumé des données créées:")
        print(f"  - Utilisateurs: {user_count}")
        print(f"  - Classes: {class_count}")
        print(f"  - Étudiants: {student_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des données de test: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    print("🏗️ Créateur de structure de base de données pour l'API formative evaluations")
    print("=" * 80)
    
    # Créer la structure
    if create_database_structure():
        print("\n🎯 Structure créée !")
        
        # Créer les données de test
        if create_test_data():
            print("\n✅ Base de données complètement configurée !")
            print("\n🔧 POUR TESTER LE FRONTEND :")
            print("1. Va sur la page de connexion")
            print("2. Connecte-toi avec:")
            print("   Email: teacher@example.com")
            print("   Mot de passe: teacher123")
            print("3. Va sur la page des évaluations formatives")
            print("4. Essaie de créer une évaluation formative")
        else:
            print("\n❌ ÉCHEC DE LA CRÉATION DES DONNÉES DE TEST")
    else:
        print("\n❌ ÉCHEC DE LA CRÉATION DE LA STRUCTURE")















