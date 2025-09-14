#!/usr/bin/env python3
"""
Script pour corriger la table adaptive_questions
"""

import sqlite3
import os

def fix_adaptive_questions_table():
    # Chemin vers la base de données
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'app.db')
    print(f"🔧 Correction de la table adaptive_questions")
    print(f"📁 Base de données: {db_path}")
    print("=" * 60)
    
    try:
        # Connexion à la base
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure actuelle
        cursor.execute("PRAGMA table_info(adaptive_questions)")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]
        
        print("📋 Colonnes actuelles:")
        for col in columns:
            print(f"  - {col[1]} ({col[2]})")
        
        # Vérifier si les nouvelles colonnes existent déjà
        needs_fix = False
        missing_columns = []
        
        required_columns = ['is_active', 'question_order', 'learning_objective']
        
        for col in required_columns:
            if col not in column_names:
                needs_fix = True
                missing_columns.append(col)
        
        if needs_fix:
            print(f"\n❌ Colonnes manquantes: {', '.join(missing_columns)}")
            print("\n🔧 Ajout des colonnes manquantes...")
            
            # Ajouter is_active si elle n'existe pas
            if 'is_active' not in column_names:
                cursor.execute("ALTER TABLE adaptive_questions ADD COLUMN is_active BOOLEAN DEFAULT 1")
                print("✅ Colonne is_active ajoutée")
            
            # Ajouter question_order si elle n'existe pas
            if 'question_order' not in column_names:
                cursor.execute("ALTER TABLE adaptive_questions ADD COLUMN question_order INTEGER DEFAULT 0")
                print("✅ Colonne question_order ajoutée")
            
            # Ajouter learning_objective si elle n'existe pas
            if 'learning_objective' not in column_names:
                cursor.execute("ALTER TABLE adaptive_questions ADD COLUMN learning_objective TEXT")
                print("✅ Colonne learning_objective ajoutée")
            
            # Mettre à jour les valeurs existantes
            print("\n🔄 Mise à jour des données existantes...")
            
            # Mettre à jour question_order depuis order_index si il existe
            if 'order_index' in column_names:
                cursor.execute("""
                    UPDATE adaptive_questions 
                    SET question_order = order_index 
                    WHERE order_index IS NOT NULL
                """)
                print("✅ question_order mis à jour depuis order_index")
            
            # Activer toutes les questions existantes
            cursor.execute("UPDATE adaptive_questions SET is_active = 1 WHERE is_active IS NULL")
            print("✅ Toutes les questions marquées comme actives")
            
            # Valider les changements
            conn.commit()
            
            # Vérifier la nouvelle structure
            print("\n📋 Nouvelle structure:")
            cursor.execute("PRAGMA table_info(adaptive_questions)")
            new_columns = cursor.fetchall()
            for col in new_columns:
                print(f"  - {col[1]} ({col[2]})")
        else:
            print("\n✅ Structure déjà correcte!")
        
        # Vérifier les données
        cursor.execute("SELECT COUNT(*) FROM adaptive_questions")
        count = cursor.fetchone()[0]
        print(f"\n📊 Nombre de questions: {count}")
        
        if count > 0:
            print("\n🔍 Aperçu des données:")
            cursor.execute("""
                SELECT id, test_id, question_text, is_active, question_order, learning_objective
                FROM adaptive_questions 
                LIMIT 3
            """)
            questions = cursor.fetchall()
            for question in questions:
                question_text = question[2][:50] + "..." if question[2] and len(question[2]) > 50 else question[2] or "N/A"
                learning_obj = question[5] or "N/A"
                print(f"ID: {question[0]}, Test: {question[1]}, Texte: {question_text}, Actif: {question[3]}, Ordre: {question[4]}, Objectif: {learning_obj}")
        
        conn.close()
        print("\n✅ Correction terminée!")
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    fix_adaptive_questions_table()

