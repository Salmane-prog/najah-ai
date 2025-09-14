#!/usr/bin/env python3
"""
Script pour créer des conversations réelles avec les vrais utilisateurs
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.orm import Session
from core.database import SessionLocal
from models.user import User, UserRole
from models.thread import Thread
from models.messages import Message
from models.class_group import ClassGroup, ClassStudent
from datetime import datetime, timedelta
import random

def create_real_conversations():
    """Créer des conversations réelles avec les vrais utilisateurs."""
    db = SessionLocal()
    
    try:
        # Récupérer le professeur principal (salmane)
        teacher = db.query(User).filter(User.username == "salmane").first()
        if not teacher:
            print("Professeur 'salmane' non trouvé.")
            return
        
        print(f"Professeur: {teacher.username} (ID: {teacher.id})")
        
        # Récupérer les classes du professeur
        classes = db.query(ClassGroup).filter(ClassGroup.teacher_id == teacher.id).all()
        if not classes:
            print("Aucune classe trouvée pour ce professeur.")
            return
        
        print(f"Classes trouvées: {len(classes)}")
        
        # Récupérer les élèves des classes du professeur
        students = db.query(User).join(ClassStudent).filter(
            ClassStudent.class_id.in_([c.id for c in classes]),
            User.role == UserRole.student
        ).distinct().all()
        
        if not students:
            print("Aucun élève trouvé dans les classes du professeur.")
            return
        
        print(f"Élèves trouvés: {len(students)}")
        for student in students:
            print(f"  - {student.username} (ID: {student.id})")
        
        # Messages de test réalistes
        teacher_messages = [
            "Bonjour ! Comment allez-vous aujourd'hui ?",
            "Avez-vous des questions sur le cours d'aujourd'hui ?",
            "N'oubliez pas de rendre votre devoir pour demain.",
            "Excellent travail sur le dernier exercice !",
            "Pouvez-vous m'expliquer ce point qui vous pose problème ?",
            "Je suis disponible pour un rendez-vous si nécessaire.",
            "Continuez comme ça, vous progressez bien !",
            "Avez-vous révisé pour le contrôle de la semaine prochaine ?",
            "Merci pour votre participation active en classe.",
            "N'hésitez pas à me poser des questions si vous avez des doutes."
        ]
        
        student_responses = [
            "Bonjour ! Je vais bien, merci !",
            "Oui, j'ai une question sur l'exercice 3.",
            "D'accord, je vais le faire ce soir.",
            "Merci beaucoup !",
            "Je vais essayer de mieux expliquer ma difficulté.",
            "Oui, je voudrais bien un rendez-vous.",
            "Merci, je vais continuer à travailler.",
            "Oui, j'ai révisé toute la semaine.",
            "Merci, c'était très intéressant.",
            "D'accord, je n'hésiterai pas."
        ]
        
        # Nettoyer les anciens threads de test
        print("Nettoyage des anciens threads de test...")
        old_threads = db.query(Thread).filter(
            Thread.created_by == teacher.id,
            Thread.title.like("%student%")
        ).all()
        
        for thread in old_threads:
            # Supprimer les messages du thread
            db.query(Message).filter(Message.thread_id == thread.id).delete()
            # Supprimer le thread
            db.delete(thread)
        
        db.commit()
        print(f"Anciens threads supprimés: {len(old_threads)}")
        
        # Créer des conversations réelles
        print("Création des conversations réelles...")
        
        for student in students:
            # Créer un thread pour chaque élève
            thread = Thread(
                title=f"Conversation avec {student.username}",
                created_by=teacher.id,
                type="teacher_student"
            )
            db.add(thread)
            db.commit()
            db.refresh(thread)
            
            print(f"Thread créé pour {student.username}: {thread.id}")
            
            # Créer quelques messages de test
            num_messages = random.randint(3, 6)
            
            for i in range(num_messages):
                # Message du professeur
                teacher_message = Message(
                    content=random.choice(teacher_messages),
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
        
        print("✅ Conversations réelles créées avec succès !")
        
    except Exception as e:
        print(f"Erreur lors de la création des conversations réelles: {str(e)}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_real_conversations() 