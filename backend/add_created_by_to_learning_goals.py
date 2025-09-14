#!/usr/bin/env python3
"""
Script pour ajouter la colonne created_by à la table learning_goals
"""

import sqlite3
import os
from pathlib import Path

def add_created_by_column():
    """Ajouter la colonne created_by à la table learning_goals"""
    
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
        
        # Vérifier si la colonne existe déjà
        cursor.execute("PRAGMA table_info(learning_goals)")
        columns = [col[1] for col in cursor.fetchall()]
        
        if 'created_by' in columns:
            print("✅ La colonne 'created_by' existe déjà dans la table learning_goals")
            return True
        
        print("📋 Colonnes actuelles de la table learning_goals:")
        for col in columns:
            print(f"  - {col}")
        
        # Ajouter la colonne created_by
        print("\n🔧 Ajout de la colonne 'created_by'...")
        cursor.execute("ALTER TABLE learning_goals ADD COLUMN created_by INTEGER")
        
        # Vérifier que la colonne a été ajoutée
        cursor.execute("PRAGMA table_info(learning_goals)")
        new_columns = [col[1] for col in cursor.fetchall()]
        
        if 'created_by' in new_columns:
            print("✅ Colonne 'created_by' ajoutée avec succès!")
            
            # Mettre à jour les enregistrements existants
            print("\n🔄 Mise à jour des enregistrements existants...")
            
            # Compter les enregistrements existants
            cursor.execute("SELECT COUNT(*) FROM learning_goals")
            count = cursor.fetchone()[0]
            print(f"📊 {count} enregistrement(s) trouvé(s)")
            
            if count > 0:
                # Pour les enregistrements existants, mettre created_by = user_id (l'étudiant qui a créé l'objectif)
                cursor.execute("UPDATE learning_goals SET created_by = user_id WHERE created_by IS NULL")
                updated = cursor.rowcount
                print(f"✅ {updated} enregistrement(s) mis à jour")
            
            # Valider les changements
            conn.commit()
            
            print("\n📋 Nouvelles colonnes de la table learning_goals:")
            cursor.execute("PRAGMA table_info(learning_goals)")
            for col in cursor.fetchall():
                print(f"  - {col[1]} ({col[2]})")
            
            return True
        else:
            print("❌ Échec de l'ajout de la colonne 'created_by'")
            return False
            
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de la colonne: {str(e)}")
        if 'conn' in locals():
            conn.rollback()
        return False
    
    finally:
        if 'conn' in locals():
            conn.close()
            print("🔌 Connexion fermée")

if __name__ == "__main__":
    print("🚀 Script d'ajout de la colonne created_by à learning_goals")
    print("=" * 60)
    
    success = add_created_by_column()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 Script exécuté avec succès!")
        print("✅ La table learning_goals a maintenant la colonne created_by")
    else:
        print("💥 Échec de l'exécution du script")
        print("❌ Vérifiez les erreurs ci-dessus")

