#!/usr/bin/env python3
"""
Script pour vérifier et corriger la table study_sessions
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import create_engine, text

def fix_study_sessions_table():
    """Vérifier et corriger la table study_sessions"""
    
    # Créer une connexion directe à la base de données
    engine = create_engine("sqlite:///../data/app.db")
    
    try:
        with engine.connect() as conn:
            # Vérifier la structure de la table
            result = conn.execute(text("PRAGMA table_info(study_sessions)"))
            columns = result.fetchall()
            
            print("📋 Structure actuelle de la table 'study_sessions':")
            for column in columns:
                print(f"   {column[1]} ({column[2]}) - {'NOT NULL' if column[3] else 'NULL'} - PK: {column[5]}")
            
            # Vérifier s'il y a des données
            result = conn.execute(text("SELECT COUNT(*) FROM study_sessions"))
            count = result.fetchone()[0]
            print(f"\n📊 Nombre de sessions d'étude: {count}")
            
            # Vérifier si l'ID est auto-incrémenté
            id_column = next((col for col in columns if col[1] == 'id'), None)
            if id_column:
                print(f"✅ Colonne ID trouvée: {id_column[2]}")
                if 'INTEGER' in id_column[2] and id_column[5] == 1:
                    print("✅ ID est bien configuré comme clé primaire auto-incrémentée")
                else:
                    print("⚠️  ID n'est pas configuré comme auto-incrémenté")
            else:
                print("❌ Colonne ID manquante")
            
            # Tester l'insertion d'une session de test
            print("\n🧪 Test d'insertion d'une session de test...")
            try:
                result = conn.execute(text("""
                    INSERT INTO study_sessions (user_id, topic, subject, start_time, end_time, planned_duration, notes, status, created_at)
                    VALUES (4, 'Test Session', 'Test Subject', '2025-01-20 10:00:00', '2025-01-20 12:00:00', 120, 'Test notes', 'planned', '2025-01-20 10:00:00')
                """))
                conn.commit()
                print("✅ Insertion de test réussie")
                
                # Récupérer l'ID généré
                result = conn.execute(text("SELECT last_insert_rowid()"))
                last_id = result.fetchone()[0]
                print(f"   ID généré: {last_id}")
                
                # Supprimer la session de test
                conn.execute(text("DELETE FROM study_sessions WHERE id = ?"), (last_id,))
                conn.commit()
                print("✅ Session de test supprimée")
                
            except Exception as e:
                print(f"❌ Erreur lors du test d'insertion: {str(e)}")
            
    except Exception as e:
        print(f"❌ Erreur: {str(e)}")

if __name__ == "__main__":
    fix_study_sessions_table() 