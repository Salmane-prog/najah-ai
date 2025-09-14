#!/usr/bin/env python3
"""
Script pour vérifier quelle table utiliser pour les évaluations formatives
"""

import sqlite3

def check_formative_tables():
    """Vérifie quelle table utiliser pour les évaluations formatives"""
    
    db_path = r"F:\IMT\stage\Yancode\Najah__AI\data\app.db"
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Rechercher les tables liées aux évaluations
        cursor.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND (
                name LIKE '%assessment%' OR 
                name LIKE '%evaluation%' OR
                name LIKE '%formative%'
            )
        """)
        
        assessment_tables = cursor.fetchall()
        
        print("🔍 Tables liées aux évaluations trouvées :")
        for table in assessment_tables:
            print(f"  - {table[0]}")
        
        # Vérifier la structure de chaque table
        for table_name in [table[0] for table in assessment_tables]:
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
                
            except Exception as e:
                print(f"    ❌ Erreur lors de la vérification : {e}")
        
        conn.close()
        
        return assessment_tables
        
    except Exception as e:
        print(f"❌ Erreur : {e}")
        return []

def suggest_best_table():
    """Suggère la meilleure table à utiliser"""
    
    print(f"\n🎯 RECOMMANDATION :")
    
    # Basé sur les noms de tables typiques
    priority_tables = [
        "formative_assessments",  # Priorité 1
        "assessments",            # Priorité 2
        "evaluations",            # Priorité 3
        "formative_evaluations"   # Priorité 4
    ]
    
    for table in priority_tables:
        print(f"   {table} - Priorité {'Haute' if table in ['formative_assessments', 'assessments'] else 'Moyenne'}")
    
    print(f"\n💡 Utilisez la table avec le nom le plus approprié pour votre cas d'usage")

if __name__ == "__main__":
    print("🔍 Vérification des tables d'évaluations formatives")
    print("=" * 80)
    
    tables = check_formative_tables()
    
    if tables:
        suggest_best_table()
    else:
        print("❌ Aucune table d'évaluation trouvée")
