#!/usr/bin/env python3
"""
Script pour vérifier les scores actuels dans la base de données
"""
import sys
import os
from sqlalchemy import text

# Ajouter le répertoire au path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def check_current_scores():
    """Vérifie les scores actuels dans quiz_results"""
    print("🔍 Vérification des scores actuels...")
    
    try:
        from core.database import SessionLocal
        
        db = SessionLocal()
        
        # 1. Compter les résultats
        total_results = db.execute(text("SELECT COUNT(*) FROM quiz_results")).scalar()
        print(f"📊 Total des résultats: {total_results}")
        
        # 2. Analyser les scores
        scores_analysis = db.execute(text("""
            SELECT 
                COUNT(*) as total,
                AVG(score) as avg_score,
                MIN(score) as min_score,
                MAX(score) as max_score,
                AVG(percentage) as avg_percentage,
                MIN(percentage) as min_percentage,
                MAX(percentage) as max_percentage
            FROM quiz_results 
            WHERE completed = 1 OR is_completed = 1
        """)).fetchone()
        
        print(f"\n📈 Analyse des scores:")
        print(f"   Total quiz complétés: {scores_analysis.total}")
        print(f"   Score moyen: {scores_analysis.avg_score:.1f}")
        print(f"   Score min: {scores_analysis.min_score}")
        print(f"   Score max: {scores_analysis.max_score}")
        print(f"   Pourcentage moyen: {scores_analysis.avg_percentage:.1f}%")
        print(f"   Pourcentage min: {scores_analysis.min_percentage:.1f}%")
        print(f"   Pourcentage max: {scores_analysis.max_percentage:.1f}%")
        
        # 3. Vérifier les scores anormaux
        abnormal_scores = db.execute(text("""
            SELECT id, score, max_score, percentage, user_id, quiz_id
            FROM quiz_results 
            WHERE percentage > 100 OR score > max_score OR percentage < 0
        """)).fetchall()
        
        print(f"\n⚠️ Scores anormaux trouvés: {len(abnormal_scores)}")
        for row in abnormal_scores:
            print(f"   ID {row.id}: Score={row.score}, Max={row.max_score}, %={row.percentage}%")
        
        # 4. Vérifier les scores avec max_score manquant
        null_max_scores = db.execute(text("""
            SELECT COUNT(*) FROM quiz_results 
            WHERE max_score IS NULL OR max_score = 0
        """)).scalar()
        
        print(f"\n❓ Scores avec max_score manquant: {null_max_scores}")
        
        # 5. Afficher quelques exemples
        print(f"\n📋 Exemples de scores:")
        examples = db.execute(text("""
            SELECT id, score, max_score, percentage, sujet
            FROM quiz_results 
            WHERE completed = 1 OR is_completed = 1
            ORDER BY created_at DESC
            LIMIT 5
        """)).fetchall()
        
        for row in examples:
            print(f"   ID {row.id}: {row.score}/{row.max_score} ({row.percentage:.1f}%) - {row.sujet}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la vérification: {e}")
        return False
    finally:
        if 'db' in locals():
            db.close()

if __name__ == "__main__":
    print("🔍 Vérification des scores de quiz...")
    print("=" * 50)
    
    if check_current_scores():
        print("\n✅ Vérification terminée!")
        print("\n💡 Si vous voyez des scores anormaux, vous pouvez:")
        print("   1. Exécuter le script fix_scores.py pour les corriger")
        print("   2. Ou les corriger manuellement dans la base de données")
    else:
        print("\n❌ Erreur lors de la vérification") 