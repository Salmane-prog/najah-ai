#!/usr/bin/env python3
"""
Script pour vérifier les tables de classes et étudiants
"""

import sqlite3

def check_classes_tables():
    """Vérifie les tables de classes et étudiants"""
    
    db_path = r"F:\IMT\stage\Yancode\Najah__AI\data\app.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Rechercher les tables liées aux classes et étudiants
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND (
                name LIKE '%class%' OR 
                name LIKE '%student%' OR
                name LIKE '%group%'
            )
        """)
        
        class_student_tables = cursor.fetchall()
        
        print("🔍 Tables de classes et étudiants trouvées :")
        for table in class_student_tables:
            print(f"  - {table[0]}")
        
        # Vérifier la structure de chaque table
        for table_name in [table[0] for table in class_student_tables]:
            print(f"\n📋 Structure de la table '{table_name}' :")
            
            try:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                for col in columns:
                    cid, name, type_name, not_null, default_val, pk = col
                    print(f"    - {name} ({type_name}) {'NOT NULL' if not_null else 'NULL'} {'PK' if pk else ''}")
                
                # Compter les enregistrements
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"    📊 Nombre d'enregistrements : {count}")
                
                # Afficher quelques exemples
                if count > 0:
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 3")
                    examples = cursor.fetchall()
                    print(f"    📝 Exemples :")
                    for i, example in enumerate(examples):
                        print(f"      {i+1}: {example}")
                
            except Exception as e:
                print(f"    ❌ Erreur lors de la vérification : {e}")
        
        conn.close()
        
        return class_student_tables
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return []

if __name__ == "__main__":
    print("🔍 Vérification des tables de classes et étudiants")
    print("=" * 80)
    
    tables = check_classes_tables()
    
    if tables:
        print(f"\n✅ Tables trouvées : {len(tables)}")
    else:
        print(f"\n❌ Aucune table trouvée")















