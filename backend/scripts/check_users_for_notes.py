#!/usr/bin/env python3
"""
Script pour vérifier les utilisateurs étudiants disponibles
"""

import sqlite3
from pathlib import Path

def check_students():
    """Vérifier les étudiants disponibles."""
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("=== VÉRIFICATION DES ÉTUDIANTS ===")
        
        # Récupérer tous les utilisateurs étudiants
        cursor.execute("""
            SELECT id, email, username, first_name, last_name, role 
            FROM users 
            WHERE role = 'student'
        """)
        
        students = cursor.fetchall()
        
        if not students:
            print("❌ Aucun étudiant trouvé dans la base de données")
            return
        
        print(f"✅ {len(students)} étudiant(s) trouvé(s):")
        print("\n📋 Liste des étudiants:")
        print("┌─────┬─────────────────────┬─────────────────────┬─────────────────────┬─────┐")
        print("│ ID  │ Email               │ Username            │ Nom complet         │ Role│")
        print("├─────┼─────────────────────┼─────────────────────┼─────────────────────┼─────┤")
        
        for student in students:
            student_id, email, username, first_name, last_name, role = student
            full_name = f"{first_name or ''} {last_name or ''}".strip() or "N/A"
            print(f"│ {student_id:3} │ {email:19} │ {username:19} │ {full_name:19} │ {role:3} │")
        
        print("└─────┴─────────────────────┴─────────────────────┴─────────────────────┴─────┘")
        
        # Suggérer un étudiant pour le test
        if students:
            test_student = students[0]
            print(f"\n🎯 Étudiant suggéré pour le test:")
            print(f"   Email: {test_student[1]}")
            print(f"   Username: {test_student[2]}")
            print(f"   ID: {test_student[0]}")
            
            # Vérifier s'il y a des notes pour cet étudiant
            cursor.execute("""
                SELECT COUNT(*) FROM notes WHERE user_id = ?
            """, (test_student[0],))
            
            notes_count = cursor.fetchone()[0]
            print(f"   Notes existantes: {notes_count}")
        
    except sqlite3.Error as e:
        print(f"❌ Erreur SQLite: {e}")
    except Exception as e:
        print(f"❌ Erreur inattendue: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    check_students() 