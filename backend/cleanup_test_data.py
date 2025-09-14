#!/usr/bin/env python3
"""
Script pour nettoyer les données de test des nouvelles fonctionnalités
⚠️ ATTENTION: Ce script supprime toutes les données de test!
"""

import sqlite3
from pathlib import Path

def cleanup_test_data():
    """Nettoyer toutes les données de test"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"📁 Base de données trouvée: {db_path}")
    print("⚠️  ATTENTION: Ce script va supprimer toutes les données de test!")
    
    # Demander confirmation
    confirm = input("\nÊtes-vous sûr de vouloir continuer? (oui/non): ").lower()
    if confirm not in ['oui', 'o', 'yes', 'y']:
        print("❌ Opération annulée par l'utilisateur")
        return False
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Tables à nettoyer (dans l'ordre pour respecter les contraintes de clés étrangères)
        tables_to_clean = [
            'ai_tutoring_interactions',
            'ai_tutoring_sessions',
            'ai_recommendations',
            'difficulty_detection',
            'group_messages',
            'group_resources',
            'study_group_members',
            'study_groups',
            'project_tasks',
            'project_members',
            'collaboration_projects',
            'homework_submissions',
            'homework_assignments',
            'detailed_reports',
            'calendar_study_sessions',
            'event_reminders',
            'calendar_events'
        ]
        
        print("\n🧹 Nettoyage des données de test...")
        
        total_deleted = 0
        
        for table in tables_to_clean:
            try:
                # Compter les enregistrements avant suppression
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count_before = cursor.fetchone()[0]
                
                if count_before > 0:
                    # Supprimer tous les enregistrements
                    cursor.execute(f"DELETE FROM {table}")
                    deleted_count = cursor.rowcount
                    total_deleted += deleted_count
                    print(f"   ✅ {table}: {deleted_count} enregistrements supprimés")
                else:
                    print(f"   ℹ️  {table}: Aucun enregistrement à supprimer")
                    
            except Exception as e:
                print(f"   ⚠️  {table}: Erreur lors de la suppression - {e}")
        
        # Validation finale
        print("\n🔍 Vérification du nettoyage...")
        
        for table in tables_to_clean:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count_after = cursor.fetchone()[0]
                if count_after == 0:
                    print(f"   ✅ {table}: Nettoyé")
                else:
                    print(f"   ⚠️  {table}: {count_after} enregistrements restants")
            except Exception as e:
                print(f"   ❌ {table}: Erreur de vérification - {e}")
        
        # Commit des changements
        conn.commit()
        print(f"\n🎉 Nettoyage terminé! {total_deleted} enregistrements supprimés au total")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du nettoyage: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("🧹 Script de nettoyage des données de test")
    print("=" * 50)
    
    success = cleanup_test_data()
    
    if success:
        print("\n✅ Nettoyage terminé avec succès!")
        print("\n💡 Prochaines étapes:")
        print("   1. Redémarrer le serveur backend")
        print("   2. Vérifier que les endpoints fonctionnent")
        print("   3. Réinsérer des données de test si nécessaire")
    else:
        print("\n❌ Erreur lors du nettoyage!")
        print("\n🔧 Actions recommandées:")
        print("   1. Vérifier les permissions de la base de données")
        print("   2. Vérifier que la base de données n'est pas verrouillée")
        print("   3. Vérifier les logs d'erreur pour plus de détails")




