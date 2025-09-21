#!/usr/bin/env python3
"""
Script d'import COMPLET des données exportées depuis JSON vers PostgreSQL
Pour restaurer toutes les données en production
"""
import os
import sys
import json
from datetime import datetime
from sqlalchemy import create_engine, text, MetaData, inspect
import logging

# Configuration du logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def import_all_data():
    """Importe toutes les données depuis les fichiers JSON d'export"""
    
    # URL de la base de données (Railway PostgreSQL)
    database_url = os.environ.get("DATABASE_URL")
    if not database_url:
        logger.error("❌ DATABASE_URL non trouvée")
        return False
    
    # Chercher tous les fichiers d'export
    import_files = []
    for filename in os.listdir('.'):
        if filename.startswith('data_export_') and filename.endswith('.json'):
            import_files.append(filename)
    
    if not import_files:
        logger.warning("⚠️ Aucun fichier d'export trouvé")
        return False
    
    logger.info(f"📂 Fichiers d'export trouvés: {import_files}")
    
    try:
        engine = create_engine(database_url)
        
        with engine.connect() as conn:
            # Vérifier si des données existent déjà
            inspector = inspect(engine)
            existing_tables = inspector.get_table_names()
            
            logger.info(f"📋 Tables existantes en base: {existing_tables}")
            
            total_imported = 0
            
            for import_file in import_files:
                logger.info(f"📥 Import depuis {import_file}")
                imported_count = import_from_file(conn, import_file)
                total_imported += imported_count
            
            logger.info(f"✅ Import terminé: {total_imported} lignes importées au total")
            return True
            
    except Exception as e:
        logger.error(f"❌ Erreur lors de l'import: {e}")
        return False

def import_from_file(conn, filename):
    """Importe les données depuis un fichier JSON spécifique"""
    
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        logger.info(f"📊 Import de {data['total_tables']} tables depuis {data['source_db']}")
        
        total_imported = 0
        
        for table_name, table_info in data["tables"].items():
            if "error" in table_info:
                logger.warning(f"⚠️ Ignorer table {table_name} (erreur lors de l'export)")
                continue
            
            table_data = table_info["data"]
            if not table_data:
                logger.info(f"📋 Table {table_name} vide, ignorée")
                continue
            
            try:
                imported_rows = import_table_data(conn, table_name, table_data)
                total_imported += imported_rows
                logger.info(f"✅ {imported_rows} lignes importées dans {table_name}")
                
            except Exception as e:
                logger.error(f"❌ Erreur import table {table_name}: {e}")
        
        return total_imported
        
    except Exception as e:
        logger.error(f"❌ Erreur lecture fichier {filename}: {e}")
        return 0

def import_table_data(conn, table_name, table_data):
    """Importe les données d'une table spécifique"""
    
    if not table_data:
        return 0
    
    # Vérifier si la table existe
    inspector = inspect(conn)
    if table_name not in inspector.get_table_names():
        logger.warning(f"⚠️ Table {table_name} n'existe pas en production, création automatique...")
        create_table_from_data(conn, table_name, table_data[0])
    
    # Préparer l'insertion
    first_row = table_data[0]
    columns = list(first_row.keys())
    
    # Créer la requête d'insertion
    placeholders = ', '.join([f':{col}' for col in columns])
    query = f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({placeholders})"
    
    inserted_count = 0
    
    for row_data in table_data:
        try:
            # Nettoyer les données (convertir None en NULL, etc.)
            cleaned_data = clean_row_data(row_data)
            conn.execute(text(query), cleaned_data)
            inserted_count += 1
            
        except Exception as e:
            logger.warning(f"⚠️ Erreur insertion ligne dans {table_name}: {e}")
    
    # Commit les changements
    conn.commit()
    
    return inserted_count

def create_table_from_data(conn, table_name, sample_row):
    """Crée une table basée sur les données d'exemple"""
    
    # Analyser les types de données
    column_definitions = []
    for col_name, col_value in sample_row.items():
        if col_value is None:
            col_type = "TEXT"
        elif isinstance(col_value, int):
            col_type = "INTEGER"
        elif isinstance(col_value, float):
            col_type = "REAL"
        elif isinstance(col_value, bool):
            col_type = "BOOLEAN"
        else:
            col_type = "TEXT"
        
        column_definitions.append(f"{col_name} {col_type}")
    
    # Créer la table
    create_query = f"CREATE TABLE IF NOT EXISTS {table_name} ({', '.join(column_definitions)})"
    
    try:
        conn.execute(text(create_query))
        conn.commit()
        logger.info(f"📋 Table {table_name} créée automatiquement")
    except Exception as e:
        logger.error(f"❌ Erreur création table {table_name}: {e}")
        raise

def clean_row_data(row_data):
    """Nettoie les données d'une ligne pour l'insertion"""
    cleaned = {}
    
    for key, value in row_data.items():
        # Convertir les chaînes vides en None
        if value == "":
            cleaned[key] = None
        # Convertir les dates ISO en format compatible
        elif isinstance(value, str) and 'T' in value and value.count('-') >= 2:
            try:
                # Tentative de parsing de date ISO
                datetime.fromisoformat(value.replace('Z', '+00:00'))
                cleaned[key] = value
            except:
                cleaned[key] = value
        else:
            cleaned[key] = value
    
    return cleaned

def create_import_summary():
    """Crée un résumé des données disponibles pour l'import"""
    
    import_files = []
    for filename in os.listdir('.'):
        if filename.startswith('data_export_') and filename.endswith('.json'):
            import_files.append(filename)
    
    if not import_files:
        print("❌ Aucun fichier d'export trouvé pour l'import")
        return
    
    print(f"📊 RÉSUMÉ DES DONNÉES DISPONIBLES POUR L'IMPORT")
    print("="*50)
    
    total_tables = 0
    total_rows = 0
    
    for filename in import_files:
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            print(f"\n📂 {filename}")
            print(f"   Source: {data['source_db']}")
            print(f"   Date export: {data['export_date']}")
            print(f"   Tables: {data['total_tables']}")
            
            file_rows = 0
            for table_name, table_info in data["tables"].items():
                row_count = table_info["row_count"]
                file_rows += row_count
                status = "✅" if "error" not in table_info else "❌"
                print(f"   {status} {table_name}: {row_count} lignes")
            
            print(f"   📈 Total: {file_rows} lignes")
            
            total_tables += data['total_tables']
            total_rows += file_rows
            
        except Exception as e:
            print(f"❌ Erreur lecture {filename}: {e}")
    
    print(f"\n🎯 TOTAL GÉNÉRAL:")
    print(f"   📋 Tables: {total_tables}")
    print(f"   📊 Lignes: {total_rows}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--summary":
        create_import_summary()
    else:
        logger.info("🚀 IMPORT COMPLET DES DONNÉES NAJAH AI")
        logger.info("="*50)
        success = import_all_data()
        if not success:
            sys.exit(1)

