from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from datetime import datetime

router = APIRouter()

@router.post("/create-adaptive-test")
async def create_test_adaptive_test(db: Session = Depends(get_db)):
    """Créer un test adaptatif de test (pour debug)"""
    try:
        # Importer les modèles ici pour éviter les conflits
        from models.adaptive_evaluation import AdaptiveTest, AdaptiveQuestion, TestAssignment
        
        # Créer un test adaptatif de test
        test = AdaptiveTest(
            title="Test Adaptatif de Test",
            subject="Français",
            description="Test adaptatif de test pour vérifier le fonctionnement",
            difficulty_min=1,
            difficulty_max=5,
            estimated_duration=20,
            total_questions=3,
            adaptation_type="hybrid",
            created_by=1
        )
        db.add(test)
        db.flush()  # Pour obtenir l'ID
        
        # Créer des questions de test
        questions_data = [
            {
                "question_text": "Quelle est la capitale de la France?",
                "options": '["Londres", "Berlin", "Paris", "Madrid"]',
                "correct_answer": "Paris",
                "difficulty_level": 2,
                "question_order": 1
            },
            {
                "question_text": "Combien de voyelles y a-t-il dans l'alphabet français?",
                "options": '["4", "5", "6", "7"]',
                "correct_answer": "6",
                "difficulty_level": 3,
                "question_order": 2
            },
            {
                "question_text": "Quel est le pluriel de 'cheval'?",
                "options": '["Chevals", "Chevaux", "Chevales", "Chevauxes"]',
                "correct_answer": "Chevaux",
                "difficulty_level": 4,
                "question_order": 3
            }
        ]
        
        for q_data in questions_data:
            question = AdaptiveQuestion(
                test_id=test.id,
                question_text=q_data["question_text"],
                options=q_data["options"],
                correct_answer=q_data["correct_answer"],
                difficulty_level=q_data["difficulty_level"],
                question_order=q_data["question_order"]
            )
            db.add(question)
        
        # Assigner le test à l'étudiant 30 (utilisateur connecté)
        assignment = TestAssignment(
            test_id=test.id,
            assignment_type="student",
            target_id=30,
            assigned_by=1,
            due_date=datetime.now(),
            status="active"
        )
        db.add(assignment)
        
        db.commit()
        
        return {
            "message": "Test adaptatif de test créé avec succès",
            "test_id": test.id,
            "title": test.title,
            "questions_count": len(questions_data),
            "assigned_to_student": 30
        }
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Erreur lors de la création du test adaptatif: {str(e)}")
