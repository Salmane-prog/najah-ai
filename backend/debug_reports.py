#!/usr/bin/env python3
"""
Script pour déboguer l'endpoint des rapports
"""

import sys
import os

# Ajouter le répertoire parent au path pour les imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from sqlalchemy import text

def debug_reports():
    """Débogue l'endpoint des rapports"""
    print("=== DÉBOGAGE DES RAPPORTS ===")
    
    db = SessionLocal()
    try:
        # Récupérer les rapports détaillés
        print("\n1. Récupération des rapports...")
        reports = db.execute(text("SELECT * FROM detailed_reports")).fetchall()
        
        print(f"Nombre de rapports: {len(reports)}")
        
        if reports:
            print("\n2. Premier rapport:")
            report = reports[0]
            print(f"  id: {report[0]}")
            print(f"  user_id: {report[1]}")
            print(f"  report_type: {report[2]}")
            print(f"  title: {report[3]}")
            print(f"  description: {report[4]}")
            print(f"  period_start: {report[5]} (type: {type(report[5])})")
            print(f"  period_end: {report[6]} (type: {type(report[6])})")
            print(f"  data: {report[7]} (type: {type(report[7])})")
            print(f"  insights: {report[8]} (type: {type(report[8])})")
            print(f"  recommendations: {report[9]} (type: {type(report[9])})")
            print(f"  is_exported: {report[10]} (type: {type(report[10])})")
            print(f"  exported_at: {report[11]} (type: {type(report[11])})")
            print(f"  created_at: {report[12]} (type: {type(report[12])})")
            
            # Tester la conversion des dates
            print("\n3. Test de conversion des dates:")
            try:
                if report[5]:
                    print(f"  period_start.isoformat(): {report[5].isoformat()}")
                else:
                    print("  period_start est None")
            except Exception as e:
                print(f"  Erreur period_start: {e}")
            
            try:
                if report[6]:
                    print(f"  period_end.isoformat(): {report[6].isoformat()}")
                else:
                    print("  period_end est None")
            except Exception as e:
                print(f"  Erreur period_end: {e}")
            
            try:
                if report[12]:
                    print(f"  created_at.isoformat(): {report[12].isoformat()}")
                else:
                    print("  created_at est None")
            except Exception as e:
                print(f"  Erreur created_at: {e}")
        
    except Exception as e:
        print(f"ERREUR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == "__main__":
    debug_reports()
