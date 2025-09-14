#!/usr/bin/env python3
"""
Script pour vérifier le contenu des tables d'évaluation adaptative
"""

import sqlite3
import os
from datetime import datetime

def check_adaptive_data():
    """Vérifie le contenu des tables d'évaluation adaptative"""
    
    db_path = 'data/app.db'
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 VÉRIFICATION DU CONTENU DES TABLES D'ÉVALUATION ADAPTATIVE")
        print("=" * 70)
        
        # 1. Vérifier les tests adaptatifs
        print("\n1️⃣ TESTS ADAPTATIFS (table adaptive_tests):")
        print("-" * 50)
        cursor.execute("""
            SELECT id, title, description, subject, difficulty_range, 
                   total_questions, estimated_duration, created_by, is_active, created_at
            FROM adaptive_tests
            ORDER BY created_at DESC
        """)
        tests = cursor.fetchall()
        
        if tests:
            print(f"   📊 {len(tests)} test(s) trouvé(s):")
            for test in tests:
                print(f"   ┌─ Test ID: {test[0]}")
                print(f"   ├─ Titre: {test[1]}")
                print(f"   ├─ Description: {test[2]}")
                print(f"   ├─ Matière: {test[3]}")
                print(f"   ├─ Difficulté: {test[4]}")
                print(f"   ├─ Questions: {test[5]}")
                print(f"   ├─ Durée: {test[6]} min")
                print(f"   ├─ Créé par: {test[7]}")
                print(f"   ├─ Actif: {test[8]}")
                print(f"   └─ Créé le: {test[9]}")
                print("   " + "─" * 40)
        else:
            print("   ❌ Aucun test adaptatif trouvé")
        
        # 2. Vérifier les attributions
        print("\n2️⃣ ATTRIBUTIONS DE TESTS (table adaptive_test_assignments):")
        print("-" * 50)
        cursor.execute("""
            SELECT id, test_id, student_id, assigned_by, status, assigned_at
            FROM adaptive_test_assignments
            ORDER BY assigned_at DESC
        """)
        assignments = cursor.fetchall()
        
        if assignments:
            print(f"   📊 {len(assignments)} attribution(s) trouvée(s):")
            for assignment in assignments:
                print(f"   ┌─ Attribution ID: {assignment[0]}")
                print(f"   ├─ Test ID: {assignment[1]}")
                print(f"   ├─ Étudiant ID: {assignment[2]}")
                print(f"   ├─ Attribué par: {assignment[3]}")
                print(f"   ├─ Statut: {assignment[4]}")
                print(f"   └─ Attribué le: {assignment[5]}")
                print("   " + "─" * 40)
        else:
            print("   ❌ Aucune attribution trouvée")
        
        # 3. Vérifier les évaluations formatives
        print("\n3️⃣ ÉVALUATIONS FORMATIVES (table formative_evaluations):")
        print("-" * 50)
        cursor.execute("""
            SELECT id, title, description, subject, evaluation_type, 
                   due_date, total_points, status, created_by, created_at
            FROM formative_evaluations
            ORDER BY created_at DESC
        """)
        evaluations = cursor.fetchall()
        
        if evaluations:
            print(f"   📊 {len(evaluations)} évaluation(s) trouvée(s):")
            for evaluation in evaluations:
                print(f"   ┌─ Évaluation ID: {evaluation[0]}")
                print(f"   ├─ Titre: {evaluation[1]}")
                print(f"   ├─ Description: {evaluation[2]}")
                print(f"   ├─ Matière: {evaluation[3]}")
                print(f"   ├─ Type: {evaluation[4]}")
                print(f"   ├─ Date limite: {evaluation[5]}")
                print(f"   ├─ Points: {evaluation[6]}")
                print(f"   ├─ Statut: {evaluation[7]}")
                print(f"   ├─ Créé par: {evaluation[8]}")
                print(f"   └─ Créé le: {evaluation[9]}")
                print("   " + "─" * 40)
        else:
            print("   ❌ Aucune évaluation formative trouvée")
        
        # 4. Vérifier les utilisateurs
        print("\n4️⃣ UTILISATEURS (table users):")
        print("-" * 50)
        cursor.execute("""
            SELECT id, email, name, role, created_at
            FROM users
            WHERE role IN ('teacher', 'student')
            ORDER BY role, created_at DESC
        """)
        users = cursor.fetchall()
        
        if users:
            print(f"   📊 {len(users)} utilisateur(s) trouvé(s):")
            for user in users:
                print(f"   ┌─ User ID: {user[0]}")
                print(f"   ├─ Email: {user[1]}")
                print(f"   ├─ Nom: {user[2]}")
                print(f"   ├─ Rôle: {user[3]}")
                print(f"   └─ Créé le: {user[4]}")
                print("   " + "─" * 40)
        else:
            print("   ❌ Aucun utilisateur trouvé")
        
        # 5. Résumé
        print("\n5️⃣ RÉSUMÉ:")
        print("-" * 50)
        print(f"   🎯 Tests adaptatifs: {len(tests)}")
        print(f"   👥 Attributions: {len(assignments)}")
        print(f"   📝 Évaluations formatives: {len(evaluations)}")
        print(f"   👤 Utilisateurs: {len(users)}")
        
        if tests:
            print(f"\n   ✅ VOS TESTS SONT BIEN STOCKÉS DANS LA BASE !")
        else:
            print(f"\n   ❌ AUCUN TEST TROUVÉ - Vérifiez la création")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")
        return False

if __name__ == "__main__":
    check_adaptive_data()
