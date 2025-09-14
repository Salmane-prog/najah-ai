#!/usr/bin/env python3
"""
Script pour vérifier les tables existantes dans la base de données
"""

import sqlite3
import os

def check_existing_tables():
    """Vérifier les tables existantes"""
    
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), 'data', 'app.db')
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return
    
    print(f"🔍 Vérification de la base: {db_path}")
    print("=" * 50)
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Récupérer toutes les tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📋 Nombre total de tables: {len(tables)}")
        print()
        
        # Tables requises pour nos widgets
        required_tables = [
            'users',
            'assessments', 
            'assessment_results',
            'learning_paths',
            'learning_path_steps',
            'student_learning_paths'
        ]
        
        print("🔍 TABLES REQUISES POUR NOS WIDGETS:")
        print("-" * 40)
        
        existing_tables = [table[0] for table in tables]
        
        for table in required_tables:
            if table in existing_tables:
                print(f"✅ {table}")
                
                # Vérifier le nombre d'enregistrements
                try:
                    cursor.execute(f"SELECT COUNT(*) FROM {table}")
                    count = cursor.fetchone()[0]
                    print(f"   📊 {count} enregistrements")
                except Exception as e:
                    print(f"   ❌ Erreur lors du comptage: {e}")
            else:
                print(f"❌ {table} - MANQUANTE")
        
        print()
        print("🔍 TOUTES LES TABLES EXISTANTES:")
        print("-" * 40)
        
        for table in existing_tables:
            print(f"📋 {table}")
            
            # Vérifier le nombre d'enregistrements
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                print(f"   📊 {count} enregistrements")
            except Exception as e:
                print(f"   ❌ Erreur lors du comptage: {e}")
        
        print()
        print("🔍 VÉRIFICATION DES DONNÉES POUR L'UTILISATEUR 30:")
        print("-" * 50)
        
        # Vérifier si l'utilisateur 30 existe
        if 'users' in existing_tables:
            try:
                cursor.execute("SELECT id, username, role FROM users WHERE id = 30")
                user = cursor.fetchone()
                if user:
                    print(f"✅ Utilisateur 30 trouvé: {user}")
                    
                    # Vérifier les évaluations
                    if 'assessments' in existing_tables:
                        cursor.execute("SELECT COUNT(*) FROM assessments WHERE student_id = 30")
                        assessment_count = cursor.fetchone()[0]
                        print(f"📊 Évaluations pour l'utilisateur 30: {assessment_count}")
                    
                    # Vérifier les parcours
                    if 'student_learning_paths' in existing_tables:
                        cursor.execute("SELECT COUNT(*) FROM student_learning_paths WHERE student_id = 30")
                        path_count = cursor.fetchone()[0]
                        print(f"📊 Parcours pour l'utilisateur 30: {path_count}")
                        
                else:
                    print("❌ Utilisateur 30 non trouvé")
            except Exception as e:
                print(f"❌ Erreur lors de la vérification de l'utilisateur 30: {e}")
        else:
            print("❌ Table 'users' manquante")
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
    
    finally:
        conn.close()

if __name__ == "__main__":
    check_existing_tables() 