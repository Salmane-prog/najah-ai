#!/usr/bin/env python3
"""
Script pour réinitialiser une évaluation
"""

from core.database import SessionLocal
from models.assessment import Assessment

def reset_assessment(assessment_id: int):
    db = SessionLocal()
    try:
        assessment = db.query(Assessment).filter(Assessment.id == assessment_id).first()
        if assessment:
            assessment.status = 'pending'
            assessment.started_at = None
            assessment.completed_at = None
            db.commit()
            print(f"✅ Évaluation {assessment_id} remise en statut 'pending'")
        else:
            print(f"❌ Évaluation {assessment_id} non trouvée")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    reset_assessment(33)
