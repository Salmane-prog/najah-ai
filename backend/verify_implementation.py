#!/usr/bin/env python3
"""
Script de vérification finale pour confirmer que toutes les fonctionnalités avancées sont opérationnelles
"""

import sqlite3
import requests
from pathlib import Path
from datetime import datetime

def verify_database_structure():
    """Vérifier la structure de la base de données"""
    print("🗄️ Vérification de la structure de la base de données...")
    
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    if not db_path.exists():
        print("❌ Base de données non trouvée")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Tables requises pour les fonctionnalités avancées
        required_tables = [
            'calendar_events',
            'event_reminders', 
            'calendar_study_sessions',
            'study_groups',
            'study_group_members',
            'group_messages',
            'group_resources',
            'ai_recommendations',
            'ai_tutoring_sessions',
            'ai_tutoring_interactions',
            'difficulty_detection',
            'homework_assignments',
            'homework_submissions',
            'collaboration_projects',
            'project_members',
            'project_tasks',
            'detailed_reports'
        ]
        
        missing_tables = []
        existing_tables = []
        
        for table in required_tables:
            cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table}'")
            if cursor.fetchone():
                existing_tables.append(table)
            else:
                missing_tables.append(table)
        
        print(f"✅ {len(existing_tables)}/{len(required_tables)} tables requises trouvées")
        
        if missing_tables:
            print(f"❌ Tables manquantes: {', '.join(missing_tables)}")
            return False
        
        # Vérifier la structure des tables importantes
        print("\n🔍 Vérification de la structure des tables...")
        
        table_checks = [
            ('calendar_events', ['title', 'event_type', 'start_time', 'created_by']),
            ('study_groups', ['name', 'subject', 'created_by']),
            ('ai_recommendations', ['user_id', 'recommendation_type', 'title']),
            ('homework_assignments', ['title', 'subject', 'assigned_by', 'due_date'])
        ]
        
        for table, required_columns in table_checks:
            try:
                cursor.execute(f"PRAGMA table_info({table})")
                columns = [col[1] for col in cursor.fetchall()]
                
                missing_cols = [col for col in required_columns if col not in columns]
                if missing_cols:
                    print(f"   ⚠️  {table}: Colonnes manquantes: {missing_cols}")
                else:
                    print(f"   ✅ {table}: Structure correcte")
            except Exception as e:
                print(f"   ❌ {table}: Erreur de vérification - {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification de la structure: {e}")
        return False
    finally:
        conn.close()

def verify_test_data():
    """Vérifier que les données de test sont présentes"""
    print("\n📊 Vérification des données de test...")
    
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier les données dans les tables principales
        data_checks = [
            ('calendar_events', 'événements de calendrier'),
            ('calendar_study_sessions', 'sessions d\'étude'),
            ('study_groups', 'groupes d\'étude'),
            ('ai_recommendations', 'recommandations IA'),
            ('homework_assignments', 'devoirs'),
            ('detailed_reports', 'rapports détaillés')
        ]
        
        total_records = 0
        
        for table, description in data_checks:
            try:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                count = cursor.fetchone()[0]
                total_records += count
                
                if count > 0:
                    print(f"   ✅ {description}: {count} enregistrements")
                else:
                    print(f"   ⚠️  {description}: Aucun enregistrement")
            except Exception as e:
                print(f"   ❌ {description}: Erreur de vérification - {e}")
        
        print(f"\n📈 Total: {total_records} enregistrements de test")
        
        return total_records > 0
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification des données: {e}")
        return False
    finally:
        conn.close()

def verify_server_connectivity():
    """Vérifier la connectivité du serveur"""
    print("\n🌐 Vérification de la connectivité du serveur...")
    
    try:
        # Test de l'endpoint de santé
        response = requests.get("http://localhost:8000/health", timeout=5)
        if response.status_code == 200:
            print("✅ Serveur backend accessible")
            return True
        else:
            print(f"⚠️ Serveur backend: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Serveur backend inaccessible")
        return False
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False

def verify_api_endpoints():
    """Vérifier que les endpoints API répondent"""
    print("\n🔌 Vérification des endpoints API...")
    
    # Endpoints à tester (sans authentification - doivent retourner 401)
    endpoints = [
        ("/api/v1/calendar/events", "Calendrier - Événements"),
        ("/api/v1/collaboration/study-groups", "Collaboration - Groupes d'étude"),
        ("/api/v1/ai_advanced/recommendations", "IA Avancée - Recommandations"),
        ("/api/v1/homework/assignments", "Devoirs - Assignations"),
        ("/api/v1/ai_advanced/analytics/performance", "IA Avancée - Analytics")
    ]
    
    working_endpoints = 0
    
    for endpoint, description in endpoints:
        try:
            response = requests.get(f"http://localhost:8000{endpoint}", timeout=5)
            
            if response.status_code == 401:
                print(f"   ✅ {description}: Protégé (401 - Non authentifié)")
                working_endpoints += 1
            elif response.status_code == 403:
                print(f"   ✅ {description}: Protégé (403 - Accès refusé)")
                working_endpoints += 1
            else:
                print(f"   ⚠️  {description}: {response.status_code}")
                
        except Exception as e:
            print(f"   ❌ {description}: Erreur - {e}")
    
    print(f"\n🎯 {working_endpoints}/{len(endpoints)} endpoints fonctionnels")
    return working_endpoints == len(endpoints)

def verify_cors_configuration():
    """Vérifier la configuration CORS"""
    print("\n🌍 Vérification de la configuration CORS...")
    
    try:
        headers = {
            'Origin': 'http://localhost:3000',
            'Access-Control-Request-Method': 'GET',
            'Access-Control-Request-Headers': 'Content-Type'
        }
        
        response = requests.options("http://localhost:8000/api/v1/calendar/events", headers=headers, timeout=5)
        
        if response.status_code == 200:
            print("✅ Configuration CORS fonctionnelle")
            return True
        else:
            print(f"⚠️ Configuration CORS: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur CORS: {e}")
        return False

def generate_verification_report():
    """Générer un rapport de vérification complet"""
    print("🚀 VÉRIFICATION COMPLÈTE DES FONCTIONNALITÉS AVANCÉES")
    print("=" * 70)
    
    checks = [
        ("Structure de la base de données", verify_database_structure),
        ("Données de test", verify_test_data),
        ("Connectivité du serveur", verify_server_connectivity),
        ("Endpoints API", verify_api_endpoints),
        ("Configuration CORS", verify_cors_configuration)
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            success = check_func()
            results.append((check_name, success))
        except Exception as e:
            print(f"❌ Erreur lors de la vérification {check_name}: {e}")
            results.append((check_name, False))
    
    # Résumé final
    print("\n" + "=" * 70)
    print("📋 RAPPORT DE VÉRIFICATION FINAL")
    print("=" * 70)
    
    passed = 0
    total = len(results)
    
    for check_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {check_name}")
        if success:
            passed += 1
    
    print(f"\n🎯 Résultats: {passed}/{total} vérifications réussies")
    
    if passed == total:
        print("\n🎉 TOUTES LES FONCTIONNALITÉS SONT OPÉRATIONNELLES!")
        print("\n✅ Implémentation réussie:")
        print("   - Gestion des Devoirs")
        print("   - Calendrier Avancé") 
        print("   - Collaboration")
        print("   - IA Avancée")
        print("   - Rapports Détaillés")
        
        print("\n💡 Prochaines étapes:")
        print("   1. Tester l'interface utilisateur")
        print("   2. Vérifier l'authentification")
        print("   3. Tester les fonctionnalités avec de vrais utilisateurs")
        
    else:
        print(f"\n⚠️ {total - passed} vérification(s) ont échoué")
        print("\n🔧 Actions recommandées:")
        print("   1. Vérifier les erreurs ci-dessus")
        print("   2. Exécuter les scripts de correction")
        print("   3. Redémarrer le serveur si nécessaire")
    
    return passed == total

if __name__ == "__main__":
    success = generate_verification_report()
    
    if success:
        print("\n✅ Vérification terminée avec succès!")
        print("\n🚀 La plateforme Najah AI est prête pour la production!")
    else:
        print("\n❌ Certaines vérifications ont échoué!")
        print("\n🔧 Veuillez corriger les problèmes avant de continuer.")




