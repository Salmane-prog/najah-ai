#!/usr/bin/env python3
"""
Script pour analyser d'où viennent réellement les données affichées dans les widgets
et comprendre pourquoi nous avons des "NaN%"
"""

import sqlite3
import os

def analyze_real_data_source():
    """Analyser la vraie source des données affichées"""
    
    db_path = "najah_ai.db"
    
    if not os.path.exists(db_path):
        print(f"❌ Base de données {db_path} non trouvée")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔍 ANALYSE DE LA VRAIE SOURCE DES DONNÉES")
        print("=" * 60)
        
        # 1. Vérifier toutes les tables
        print("\n1. 📊 TOUTES LES TABLES DISPONIBLES")
        print("-" * 40)
        
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        for i, (table_name,) in enumerate(tables, 1):
            print(f"   {i:2d}. {table_name}")
        
        # 2. Analyser les tables qui pourraient contenir des données d'étudiants
        print("\n2. 🎯 ANALYSE DES TABLES POTENTIELLES")
        print("-" * 40)
        
        # Vérifier test_attempts (pour les tentatives de tests)
        print("\n   📝 TABLE test_attempts:")
        try:
            cursor.execute("SELECT COUNT(*) FROM test_attempts WHERE student_id = 30")
            count = cursor.fetchone()[0]
            print(f"      Tentatives pour l'étudiant 30: {count}")
            
            if count > 0:
                cursor.execute("""
                    SELECT test_id, started_at, completed_at, score
                    FROM test_attempts 
                    WHERE student_id = 30 
                    LIMIT 3
                """)
                attempts = cursor.fetchall()
                for attempt in attempts:
                    print(f"      Test {attempt[0]}, Score: {attempt[3]}, Started: {attempt[1]}")
        except Exception as e:
            print(f"      ❌ Erreur: {e}")
        
        # Vérifier adaptive_sessions (pour les sessions adaptatives)
        print("\n   🧠 TABLE adaptive_sessions:")
        try:
            cursor.execute("SELECT COUNT(*) FROM adaptive_sessions WHERE student_id = 30")
            count = cursor.fetchone()[0]
            print(f"      Sessions pour l'étudiant 30: {count}")
            
            if count > 0:
                cursor.execute("""
                    SELECT session_start, session_end, initial_difficulty, final_difficulty
                    FROM adaptive_sessions 
                    WHERE student_id = 30 
                    LIMIT 3
                """)
                sessions = cursor.fetchall()
                for session in sessions:
                    print(f"      Session: {session[0]} à {session[1]}, Difficulté: {session[2]}→{session[3]}")
        except Exception as e:
            print(f"      ❌ Erreur: {e}")
        
        # Vérifier cognitive_profiles (pour les profils cognitifs)
        print("\n   🧩 TABLE cognitive_profiles:")
        try:
            cursor.execute("SELECT COUNT(*) FROM cognitive_profiles WHERE student_id = 30")
            count = cursor.fetchone()[0]
            print(f"      Profils pour l'étudiant 30: {count}")
            
            if count > 0:
                cursor.execute("""
                    SELECT learning_style, strengths, weaknesses
                    FROM cognitive_profiles 
                    WHERE student_id = 30
                """)
                profiles = cursor.fetchall()
                for profile in profiles:
                    print(f"      Style: {profile[0]}, Forces: {profile[1]}")
        except Exception as e:
            print(f"      ❌ Erreur: {e}")
        
        # 3. Vérifier les endpoints qui fonctionnent réellement
        print("\n3. 🌐 ENDPOINTS QUI FONCTIONNENT RÉELLEMENT")
        print("-" * 40)
        
        print("   📍 Endpoints utilisés par les widgets:")
        print("      - /api/v1/french-optimized/student/{id}/profile")
        print("      - /api/v1/student_learning_paths/student/{id}")
        
        print("\n   🔍 Tables correspondantes:")
        print("      - french-optimized → Pas de table directe")
        print("      - student_learning_paths → Table vide")
        
        # 4. Analyser pourquoi les widgets affichent des données
        print("\n4. 🤔 POURQUOI LES WIDGETS AFFICHENT DES DONNÉES ?")
        print("-" * 40)
        
        print("   🎭 HYPOTHÈSES:")
        print("      1. Les données viennent d'endpoints différents")
        print("      2. Les données sont simulées dans le frontend")
        print("      3. Les données viennent de tables non identifiées")
        print("      4. Les données sont mises en cache quelque part")
        
        # 5. Vérifier s'il y a des données cachées
        print("\n5. 🔍 RECHERCHE DE DONNÉES CACHÉES")
        print("-" * 40)
        
        # Vérifier toutes les tables pour des données d'étudiant 30
        for table_name, in tables:
            try:
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                
                # Chercher des colonnes qui pourraient contenir student_id
                student_columns = [col for col in columns if 'student' in col[1].lower() or 'user' in col[1].lower()]
                
                if student_columns:
                    print(f"   📋 {table_name}:")
                    for col in student_columns:
                        print(f"      Colonne: {col[1]} ({col[2]})")
                        
                        # Vérifier s'il y a des données pour l'étudiant 30
                        try:
                            cursor.execute(f"SELECT COUNT(*) FROM {table_name} WHERE {col[1]} = 30")
                            count = cursor.fetchone()[0]
                            print(f"      Données pour étudiant 30: {count}")
                            
                            if count > 0:
                                cursor.execute(f"SELECT * FROM {table_name} WHERE {col[1]} = 30 LIMIT 1")
                                sample = cursor.fetchone()
                                print(f"      Exemple: {sample}")
                        except Exception as e:
                            print(f"      ❌ Erreur lors de la vérification: {e}")
                    
                    print()
                    
            except Exception as e:
                continue
        
        conn.close()
        
        print("\n   🎯 Analyse terminée!")
        print("   💡 Les widgets affichent probablement des données simulées ou d'endpoints différents")
        
    except Exception as e:
        print(f"💥 Erreur lors de l'analyse: {e}")

if __name__ == "__main__":
    analyze_real_data_source()
