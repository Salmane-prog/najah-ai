#!/usr/bin/env python3
import sqlite3

def check_all_tables():
    try:
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()
        
        print('=== TOUTES LES TABLES EXISTANTES ===')
        
        # Vérifier toutes les tables existantes
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        if not tables:
            print('❌ Aucune table trouvée dans la base de données')
            return
        
        print(f'Nombre total de tables: {len(tables)}')
        print('\nTables trouvées:')
        for i, table in enumerate(tables, 1):
            print(f'  {i}. {table[0]}')
        
        print('\n=== ANALYSE DÉTAILLÉE DE CHAQUE TABLE ===')
        
        for table in tables:
            table_name = table[0]
            print(f'\n--- TABLE: {table_name} ---')
            
            try:
                # Compter les enregistrements
                cursor.execute(f'SELECT COUNT(*) FROM {table_name}')
                count = cursor.fetchone()[0]
                print(f'Enregistrements: {count}')
                
                if count > 0:
                    # Afficher la structure de la table
                    cursor.execute(f'PRAGMA table_info({table_name})')
                    columns = cursor.fetchall()
                    print('Colonnes:')
                    for col in columns:
                        print(f'  - {col[1]} ({col[2]})')
                    
                    # Afficher quelques exemples de données
                    cursor.execute(f'SELECT * FROM {table_name} LIMIT 3')
                    rows = cursor.fetchall()
                    print('Exemples de données:')
                    for i, row in enumerate(rows):
                        print(f'  {i+1}: {row}')
                else:
                    print('  ❌ Table vide')
                    
            except Exception as e:
                print(f'  ❌ Erreur lors de l\'analyse: {e}')
        
        conn.close()
        
    except Exception as e:
        print('❌ Erreur de connexion à la base de données:', e)

if __name__ == "__main__":
    check_all_tables()





