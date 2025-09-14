#!/usr/bin/env python3
"""
Script pour mettre à jour la table quiz_assignments avec les nouveaux champs
"""

import sqlite3
import os
from pathlib import Path

def update_quiz_assignments_table():
    """Mettre à jour la table quiz_assignments avec les nouveaux champs"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print(f"🔗 Connexion à la base de données: {db_path}")
        
        # Vérifier la structure actuelle de la table
        cursor.execute("PRAGMA table_info(quiz_assignments)")
        current_columns = [col[1] for col in cursor.fetchall()]
        
        print("📋 Colonnes actuelles de la table quiz_assignments:")
        for col in current_columns:
            print(f"  - {col}")
        
        # Ajouter les nouveaux champs s'ils n'existent pas
        new_fields = [
            ("assigned_by", "INTEGER"),
            ("status", "TEXT"),
            ("score", "INTEGER"),
            ("completed_at", "TIMESTAMP"),
            ("feedback", "TEXT")
        ]
        
        for field_name, field_type in new_fields:
            if field_name not in current_columns:
                print(f"\n🔧 Ajout de la colonne '{field_name}'...")
                cursor.execute(f"ALTER TABLE quiz_assignments ADD COLUMN {field_name} {field_type}")
                print(f"✅ Colonne '{field_name}' ajoutée")
            else:
                print(f"✅ Colonne '{field_name}' existe déjà")
        
        # Mettre à jour les valeurs par défaut
        print("\n🔄 Mise à jour des valeurs par défaut...")
        
        # Mettre assigned_by = 1 (admin) pour les enregistrements existants
        if 'assigned_by' in current_columns:
            cursor.execute("UPDATE quiz_assignments SET assigned_by = 1 WHERE assigned_by IS NULL")
            updated = cursor.rowcount
            if updated > 0:
                print(f"✅ {updated} enregistrement(s) mis à jour avec assigned_by = 1")
        
        # Mettre status = 'assigned' pour les enregistrements existants
        if 'status' in current_columns:
            cursor.execute("UPDATE quiz_assignments SET status = 'assigned' WHERE status IS NULL")
            updated = cursor.rowcount
            if updated > 0:
                print(f"✅ {updated} enregistrement(s) mis à jour avec status = 'assigned'")
        
        # Valider les changements
        conn.commit()
        
        # Vérifier la nouvelle structure
        cursor.execute("PRAGMA table_info(quiz_assignments)")
        new_columns = [col[1] for col in cursor.fetchall()]
        
        print("\n📋 Nouvelles colonnes de la table quiz_assignments:")
        for col in new_columns:
            print(f"  - {col}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()
            print("🔌 Connexion fermée")

if __name__ == "__main__":
    print("🚀 Script de mise à jour de la table quiz_assignments")
    print("=" * 60)
    
    success = update_quiz_assignments_table()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Script exécuté avec succès!")
        print("✅ La table quiz_assignments a été mise à jour")
    else:
        print("💥 Échec de l'exécution du script")
        print("❌ Vérifiez les erreurs ci-dessus")
