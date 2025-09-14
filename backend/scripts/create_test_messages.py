#!/usr/bin/env python3
"""
Script pour créer des données de test pour la messagerie
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from core.database import SessionLocal, engine
from models.user import User, UserRole
from models.thread import Thread
from models.messages import Message
from models.class_group import ClassGroup, ClassStudent
from datetime import datetime, timedelta
import random

def create_test_messages():
    """Créer des messages de test pour la messagerie."""
    db = SessionLocal()
    
    try:
        # Récupérer un professeur
        teacher = db.query(User).filter(User.role == UserRole.teacher).first()
        if not teacher:
            print("Aucun professeur trouvé. Créez d'abord un professeur.")
            return
        
        # Récupérer les classes du professeur
        classes = db.query(ClassGroup).filter(ClassGroup.teacher_id == teacher.id).all()
        if not classes:
            print("Aucune classe trouvée pour ce professeur.")
            return
        
        # Récupérer les élèves
        students = db.query(User).join(ClassStudent).filter(
            ClassStudent.class_id.in_([c.id for c in classes]),
            User.role == UserRole.student
        ).all()
        
        if not students:
            print("Aucun élève trouvé dans les classes du professeur.")
            return
        
        print(f"Création de messages de test pour {len(students)} élèves...")
        
        # Messages de test
        test_messages = [
            "Bonjour, comment allez-vous ?",
            "Avez-vous des questions sur le cours ?",
            "N'oubliez pas de rendre votre devoir pour demain.",
            "Excellent travail sur le dernier exercice !",
            "Pouvez-vous m'expliquer ce point ?",
            "Je suis disponible pour un rendez-vous si nécessaire.",
            "Continuez comme ça, vous progressez bien !",
            "Avez-vous révisé pour le contrôle ?",
            "Merci pour votre participation en classe.",
            "N'hésitez pas à me poser des questions."
        ]
        
        # Réponses des élèves
        student_responses = [
            "Merci, je vais bien !",
            "Oui, j'ai une question sur l'exercice 3.",
            "D'accord, je vais le faire ce soir.",
            "Merci beaucoup !",
            "Je vais essayer de mieux expliquer.",
            "Oui, je voudrais bien un rendez-vous.",
            "Merci, je vais continuer à travailler.",
            "Oui, j'ai révisé toute la semaine.",
            "Merci, c'était très intéressant.",
            "D'accord, je n'hésiterai pas."
        ]
        
        for student in students:
            # Créer un thread pour chaque élève
            thread = db.query(Thread).filter(
                Thread.created_by == teacher.id,
                Thread.title.like(f"%{student.username}%")
            ).first()
            
            if not thread:
                thread = Thread(
                    title=f"Conversation avec {student.username}",
                    created_by=teacher.id,
                    type="teacher_student"
                )
                db.add(thread)
                db.commit()
                db.refresh(thread)
            
            # Créer quelques messages de test
            for i in range(random.randint(2, 5)):
                # Message du professeur
                teacher_message = Message(
                    content=random.choice(test_messages),
                    user_id=teacher.id,
                    thread_id=thread.id,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(1, 7), hours=random.randint(1, 12)),
                    is_read=True
                )
                db.add(teacher_message)
                
                # Réponse de l'élève
                student_message = Message(
                    content=random.choice(student_responses),
                    user_id=student.id,
                    thread_id=thread.id,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 6), hours=random.randint(1, 12)),
                    is_read=random.choice([True, False])
                )
                db.add(student_message)
            
            db.commit()
            print(f"Messages créés pour {student.username}")
        
        print("✅ Messages de test créés avec succès !")
        
    except Exception as e:
        print(f"Erreur lors de la création des messages de test: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_messages() 