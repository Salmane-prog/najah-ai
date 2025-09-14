import sqlite3
import os

def add_attachment_column():
    """Ajouter la colonne attachment à la table assignments"""
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier si la colonne existe déjà
        cursor.execute("PRAGMA table_info(assignments)")
        columns = [column[1] for column in cursor.fetchall()]
        
        if 'attachment' in columns:
            print("✅ La colonne 'attachment' existe déjà dans la table 'assignments'")
            return True
        
        # Ajouter la colonne attachment
        cursor.execute("""
            ALTER TABLE assignments 
            ADD COLUMN attachment TEXT
        """)
        
        # Valider les changements
        conn.commit()
        
        print("✅ Colonne 'attachment' ajoutée avec succès à la table 'assignments'")
        
        # Vérifier que la colonne a été ajoutée
        cursor.execute("PRAGMA table_info(assignments)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 Colonnes actuelles: {columns}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'ajout de la colonne: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔄 Ajout de la colonne 'attachment' à la table 'assignments'...")
    success = add_attachment_column()
    
    if success:
        print("🎉 Opération terminée avec succès !")
    else:
        print("💥 Échec de l'opération !")
