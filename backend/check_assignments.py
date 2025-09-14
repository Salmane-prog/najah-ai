import sqlite3
import json

def check_assignments():
    """Vérifier le contenu de la table assignments"""
    
    # Chemin vers la base de données
    db_path = "../data/app.db"
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Vérifier la structure de la table
        cursor.execute("PRAGMA table_info(assignments)")
        columns = [column[1] for column in cursor.fetchall()]
        print(f"📋 Colonnes de la table assignments: {columns}")
        
        # Vérifier les derniers assignments
        cursor.execute("SELECT id, title, attachment FROM assignments ORDER BY id DESC LIMIT 5")
        rows = cursor.fetchall()
        
        print(f"\n📝 Derniers assignments:")
        for row in rows:
            assignment_id, title, attachment = row
            print(f"  ID: {assignment_id}, Title: {title}")
            if attachment:
                try:
                    # Essayer de parser le JSON
                    attachment_data = json.loads(attachment)
                    print(f"    Attachment: {attachment_data}")
                except json.JSONDecodeError:
                    print(f"    Attachment (raw): {attachment}")
            else:
                print(f"    Attachment: NULL")
        
        # Vérifier spécifiquement les assignments avec attachment
        cursor.execute("SELECT COUNT(*) FROM assignments WHERE attachment IS NOT NULL")
        count_with_attachment = cursor.fetchone()[0]
        print(f"\n📊 Total assignments avec attachment: {count_with_attachment}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🔍 Vérification de la table assignments...")
    success = check_assignments()
    
    if success:
        print("\n✅ Vérification terminée !")
    else:
        print("\n💥 Échec de la vérification !")


