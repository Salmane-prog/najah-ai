#!/usr/bin/env python3
"""
Script pour tester la messagerie
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
from datetime import datetime

def test_messaging():
    """Tester la messagerie."""
    db = SessionLocal()
    
    try:
        print("=== TEST DE LA MESSAGERIE ===")
        
        # Vérifier les professeurs
        teachers = db.query(User).filter(User.role == UserRole.teacher).all()
        print(f"Professeurs trouvés: {len(teachers)}")
        for teacher in teachers:
            print(f"  - {teacher.username} (ID: {teacher.id})")
        
        # Vérifier les élèves
        students = db.query(User).filter(User.role == UserRole.student).all()
        print(f"Élèves trouvés: {len(students)}")
        for student in students:
            print(f"  - {student.username} (ID: {student.id})")
        
        # Vérifier les threads
        threads = db.query(Thread).all()
        print(f"Threads trouvés: {len(threads)}")
        for thread in threads:
            creator = db.query(User).filter(User.id == thread.created_by).first()
            print(f"  - Thread {thread.id}: {thread.title} (créé par {creator.username if creator else 'Unknown'})")
            
            # Compter les messages dans ce thread
            message_count = db.query(Message).filter(Message.thread_id == thread.id).count()
            print(f"    Messages: {message_count}")
            
            # Dernier message
            last_message = db.query(Message).filter(Message.thread_id == thread.id).order_by(Message.created_at.desc()).first()
            if last_message:
                sender = db.query(User).filter(User.id == last_message.user_id).first()
                print(f"    Dernier message: '{last_message.content[:50]}...' par {sender.username if sender else 'Unknown'}")
        
        # Vérifier les messages non lus
        unread_messages = db.query(Message).filter(Message.is_read == False).count()
        print(f"Messages non lus: {unread_messages}")
        
        # Vérifier les conversations par professeur
        for teacher in teachers:
            print(f"\n=== CONVERSATIONS DE {teacher.username.upper()} ===")
            teacher_threads = db.query(Thread).filter(Thread.created_by == teacher.id).all()
            print(f"Threads: {len(teacher_threads)}")
            
            for thread in teacher_threads:
                # Trouver l'élève dans le titre du thread
                student_name = thread.title.replace("Conversation avec ", "")
                student = db.query(User).filter(User.username == student_name).first()
                
                if student:
                    message_count = db.query(Message).filter(Message.thread_id == thread.id).count()
                    unread_count = db.query(Message).filter(
                        Message.thread_id == thread.id,
                        Message.user_id == student.id,
                        Message.is_read == False
                    ).count()
                    
                    print(f"  - {student.username}: {message_count} messages, {unread_count} non lus")
        
        print("\n✅ Test de la messagerie terminé !")
        
    except Exception as e:
        print(f"Erreur lors du test: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    test_messaging() 