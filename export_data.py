#!/usr/bin/env python3
"""
Script d'export COMPLET de toutes les tables et données depuis SQLite vers JSON
pour pouvoir les réimporter en production
"""
import sqlite3
import json
from datetime import datetime
import os
import sys

def export_sqlite_data():
    """Exporte TOUTES les données depuis SQLite"""
    
    # Fichiers de base de données SQLite
    db_files = ['app.db', 'najah_ai.db', 'data/app.db', 'backend/app.db', 'backend/najah_ai.db']
    
    exported_files = []
    
    for db_file in db_files:
        if os.path.exists(db_file):
            print(f"📂 Analyse de {db_file}...")
            # Compter les tables avant l'export
            try:
                conn = sqlite3.connect(db_file)
                tables = get_all_tables(conn)
                conn.close()
                print(f"   📋 {len(tables)} tables détectées")
                print(f"📂 Export depuis {db_file}")
                success = export_from_db(db_file)
                if success:
                    exported_files.append(db_file)
            except Exception as e:
                print(f"   ❌ Erreur analyse {db_file}: {e}")
    
    if not exported_files:
        print("❌ Aucun fichier de base de données trouvé")
        print("🔍 Recherche dans tous les sous-dossiers...")
        find_all_db_files()
    else:
        print(f"✅ Export terminé depuis {len(exported_files)} base(s) de données")

def find_all_db_files():
    """Trouve tous les fichiers .db dans le projet"""
    db_files = []
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.db') or file.endswith('.sqlite') or file.endswith('.sqlite3'):
                db_path = os.path.join(root, file)
                db_files.append(db_path)
                print(f"🔍 Trouvé: {db_path}")
    
    if db_files:
        print(f"\n📊 {len(db_files)} fichier(s) de base trouvé(s)")
        for db_file in db_files:
            print(f"📂 Analyse de {db_file}...")
            # Compter les tables avant l'export
            try:
                conn = sqlite3.connect(db_file)
                tables = get_all_tables(conn)
                conn.close()
                print(f"   📋 {len(tables)} tables détectées")
                print(f"📂 Export depuis {db_file}")
                export_from_db(db_file)
            except Exception as e:
                print(f"   ❌ Erreur analyse {db_file}: {e}")
    else:
        print("❌ Aucun fichier de base de données trouvé dans le projet")

def get_all_tables(conn):
    """Récupère toutes les tables de la base de données"""
    cursor = conn.execute("""
        SELECT name FROM sqlite_master 
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    return [row[0] for row in cursor.fetchall()]

def export_from_db(db_path):
    """Exporte TOUTES les données depuis une base SQLite spécifique"""
    
    try:
        conn = sqlite3.connect(db_path)
        conn.row_factory = sqlite3.Row  # Pour avoir les noms de colonnes
        
        # Récupérer toutes les tables
        tables = get_all_tables(conn)
        
        if not tables:
            print(f"⚠️ Aucune table trouvée dans {db_path}")
            conn.close()
            return False
        
        print(f"📋 {len(tables)} tables trouvées: {', '.join(tables)}")
        
        export_data = {
            "export_date": datetime.now().isoformat(),
            "source_db": db_path,
            "total_tables": len(tables),
            "table_names": tables,
            "tables": {}
        }
        
        total_rows = 0
        
        # Exporter chaque table
        for table_name in tables:
            try:
                print(f"📊 Export de la table '{table_name}'...")
                
                # Récupérer toutes les données de la table
                cursor = conn.execute(f"SELECT * FROM {table_name}")
                rows = cursor.fetchall()
                
                # Convertir en dictionnaires
                table_data = []
                for row in rows:
                    table_data.append(dict(row))
                
                export_data["tables"][table_name] = {
                    "row_count": len(table_data),
                    "data": table_data
                }
                
                total_rows += len(table_data)
                print(f"✅ {len(table_data)} lignes exportées depuis '{table_name}'")
                
            except Exception as e:
                print(f"❌ Erreur export table '{table_name}': {e}")
                export_data["tables"][table_name] = {
                    "error": str(e),
                    "row_count": 0,
                    "data": []
                }
        
        # Nom du fichier d'export basé sur le nom de la base
        db_name = os.path.basename(db_path).replace('.', '_')
        export_filename = f'data_export_{db_name}.json'
        
        # Sauvegarder en JSON
        with open(export_filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📄 {total_rows} lignes exportées dans {export_filename}")
        print(f"📊 Résumé: {len(tables)} tables, {total_rows} lignes au total")
        
        # Créer aussi un résumé
        create_summary(export_data, f'summary_{db_name}.txt')
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'export de {db_path}: {e}")
        return False

def create_summary(export_data, filename):
    """Crée un résumé de l'export"""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"📊 RÉSUMÉ DE L'EXPORT - {export_data['export_date']}\n")
            f.write(f"{'='*50}\n\n")
            f.write(f"Source: {export_data['source_db']}\n")
            f.write(f"Nombre total de tables: {export_data['total_tables']}\n\n")
            
            total_rows = 0
            for table_name, table_info in export_data["tables"].items():
                row_count = table_info["row_count"]
                total_rows += row_count
                status = "✅" if "error" not in table_info else "❌"
                f.write(f"{status} {table_name}: {row_count} lignes\n")
            
            f.write(f"\n📈 TOTAL: {total_rows} lignes exportées\n")
        
        print(f"📋 Résumé créé: {filename}")
        
    except Exception as e:
        print(f"⚠️ Erreur création résumé: {e}")

if __name__ == "__main__":
    print("🚀 EXPORT COMPLET DES BASES DE DONNÉES NAJAH AI")
    print("="*50)
    export_sqlite_data()
