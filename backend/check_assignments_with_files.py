import sqlite3
import json
from pathlib import Path

def check_assignments_with_files():
    """Vérifier quels devoirs ont des fichiers attachés"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    try:
        # Connexion à la base de données
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 Vérification des devoirs avec fichiers...")
        
        # Vérifier tous les devoirs
        cursor.execute("SELECT id, title, attachment FROM assignments ORDER BY id DESC")
        assignments = cursor.fetchall()
        
        print(f"\n📝 Total des devoirs: {len(assignments)}")
        
        assignments_with_files = []
        assignments_without_files = []
        
        for assignment_id, title, attachment in assignments:
            if attachment:
                try:
                    attachment_data = json.loads(attachment)
                    assignments_with_files.append({
                        'id': assignment_id,
                        'title': title,
                        'attachment': attachment_data
                    })
                    print(f"✅ Devoir {assignment_id}: '{title}' - Fichier: {attachment_data.get('name', 'N/A')}")
                except json.JSONDecodeError:
                    print(f"⚠️ Devoir {assignment_id}: '{title}' - Attachment invalide: {attachment}")
            else:
                assignments_without_files.append({
                    'id': assignment_id,
                    'title': title
                })
                print(f"❌ Devoir {assignment_id}: '{title}' - Aucun fichier")
        
        print(f"\n📊 Résumé:")
        print(f"  - Devoirs avec fichiers: {len(assignments_with_files)}")
        print(f"  - Devoirs sans fichiers: {len(assignments_without_files)}")
        
        if assignments_with_files:
            print(f"\n🎯 Devoirs avec fichiers (pour tester):")
            for assignment in assignments_with_files[:3]:  # Afficher les 3 premiers
                print(f"  - ID: {assignment['id']}, Titre: '{assignment['title']}'")
                print(f"    Fichier: {assignment['attachment'].get('name', 'N/A')}")
                print(f"    URL: {assignment['attachment'].get('url', 'N/A')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False
        
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    print("🚀 Vérification des devoirs avec fichiers...")
    success = check_assignments_with_files()
    
    if success:
        print("\n✅ Vérification terminée !")
    else:
        print("\n💥 Échec de la vérification !")
