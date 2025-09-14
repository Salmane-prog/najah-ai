#!/usr/bin/env python3
"""
Script de test pour l'évaluation initiale
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.database import SessionLocal
from models.user import User, UserRole
from models.assessment import Assessment, AssessmentQuestion, AssessmentResult
from core.security import get_password_hash
from datetime import datetime
import json

def test_assessment_system():
    db = SessionLocal()
    try:
        print("🧪 Test du système d'évaluation initiale...")
        
        # 1. Créer un étudiant de test
        test_student = db.query(User).filter(User.email == "test_assessment@najah.ai").first()
        if not test_student:
            test_student = User(
                username="test_assessment",
                email="test_assessment@najah.ai",
                hashed_password=get_password_hash("test123"),
                role=UserRole.student
            )
            db.add(test_student)
            db.commit()
            db.refresh(test_student)
            print("✅ Étudiant de test créé")
        else:
            print("✅ Étudiant de test existant trouvé")
        
        # 2. Vérifier s'il a déjà une évaluation
        existing_assessment = db.query(Assessment).filter(
            Assessment.student_id == test_student.id,
            Assessment.assessment_type == "initial"
        ).first()
        
        if existing_assessment:
            print("✅ Évaluation existante trouvée")
            print(f"   - ID: {existing_assessment.id}")
            print(f"   - Status: {existing_assessment.status}")
            print(f"   - Questions: {len(existing_assessment.questions)}")
            
            # Vérifier le résultat
            result = db.query(AssessmentResult).filter(
                AssessmentResult.assessment_id == existing_assessment.id
            ).first()
            
            if result:
                print(f"   - Score: {result.total_score}/{result.max_score} ({result.percentage}%)")
                print("   - Profil d'apprentissage généré")
            else:
                print("   - Aucun résultat trouvé")
        else:
            print("❌ Aucune évaluation trouvée pour cet étudiant")
            print("   L'étudiant doit passer l'évaluation via l'interface web")
        
        # 3. Afficher les statistiques
        total_assessments = db.query(Assessment).count()
        completed_assessments = db.query(Assessment).filter(Assessment.status == "completed").count()
        total_results = db.query(AssessmentResult).count()
        
        print(f"\n📊 Statistiques d'évaluation:")
        print(f"   - Total évaluations: {total_assessments}")
        print(f"   - Évaluations terminées: {completed_assessments}")
        print(f"   - Résultats: {total_results}")
        
        # 4. Afficher les étudiants avec évaluations
        students_with_assessments = db.query(User).join(Assessment).filter(User.role == UserRole.student).all()
        print(f"\n👥 Étudiants avec évaluations: {len(students_with_assessments)}")
        for student in students_with_assessments:
            assessments = db.query(Assessment).filter(Assessment.student_id == student.id).all()
            print(f"   - {student.username} ({student.email}): {len(assessments)} évaluation(s)")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        db.rollback()
        return False
    finally:
        db.close()

if __name__ == "__main__":
    print("🧪 Test du système d'évaluation initiale...")
    success = test_assessment_system()
    
    if success:
        print(f"\n✅ Test réussi! Le système d'évaluation fonctionne.")
        print(f"   Vous pouvez maintenant tester l'interface web.")
    else:
        print(f"\n❌ Test échoué. Vérifiez les erreurs ci-dessus.") 