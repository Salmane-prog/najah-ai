#!/usr/bin/env python3
"""
Script pour vérifier directement dans la base de données les données de messagerie
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

def check_messaging_database():
    """Vérifier les données de messagerie dans la base de données."""
    db = SessionLocal()
    
    try:
        print("=== VÉRIFICATION DES DONNÉES DE MESSAGERIE DANS LA BASE ===")
        
        # 1. Vérifier les utilisateurs
        print("\n1. UTILISATEURS:")
        users = db.query(User).all()
        print(f"Total utilisateurs: {len(users)}")
        
        teachers = db.query(User).filter(User.role == UserRole.teacher).all()
        students = db.query(User).filter(User.role == UserRole.student).all()
        
        print(f"Professeurs: {len(teachers)}")
        for teacher in teachers:
            print(f"  - {teacher.username} (ID: {teacher.id}) - {teacher.email}")
            
        print(f"Étudiants: {len(students)}")
        for student in students:
            print(f"  - {student.username} (ID: {student.id}) - {student.email}")
        
        # 2. Vérifier les threads/conversations
        print("\n2. THREADS/CONVERSATIONS:")
        threads = db.query(Thread).all()
        print(f"Total threads: {len(threads)}")
        
        for thread in threads:
            creator = db.query(User).filter(User.id == thread.created_by).first()
            print(f"  - Thread {thread.id}: '{thread.title}' (créé par {creator.username if creator else 'Unknown'})")
            print(f"    Type: {thread.type}")
            print(f"    Créé le: {thread.created_at}")
            
            # Compter les messages dans ce thread
            message_count = db.query(Message).filter(Message.thread_id == thread.id).count()
            print(f"    Messages: {message_count}")
        
        # 3. Vérifier les messages
        print("\n3. MESSAGES:")
        messages = db.query(Message).all()
        print(f"Total messages: {len(messages)}")
        
        # Messages par thread
        for thread in threads:
            thread_messages = db.query(Message).filter(Message.thread_id == thread.id).order_by(Message.created_at).all()
            if thread_messages:
                print(f"\n  Thread {thread.id} - '{thread.title}':")
                for msg in thread_messages:
                    sender = db.query(User).filter(User.id == msg.user_id).first()
                    print(f"    - {sender.username if sender else 'Unknown'}: '{msg.content[:50]}...' ({msg.created_at})")
                    print(f"      Lu: {msg.is_read}")
        
        # 4. Vérifier les classes et relations
        print("\n4. CLASSES ET RELATIONS:")
        classes = db.query(ClassGroup).all()
        print(f"Total classes: {len(classes)}")
        
        for class_group in classes:
            teacher = db.query(User).filter(User.id == class_group.teacher_id).first()
            students_in_class = db.query(ClassStudent).filter(ClassStudent.class_id == class_group.id).count()
            print(f"  - Classe {class_group.id}: '{class_group.name}' (Prof: {teacher.username if teacher else 'Unknown'}, {students_in_class} étudiants)")
        
        # 5. Vérifier les conversations spécifiques
        print("\n5. CONVERSATIONS SPÉCIFIQUES:")
        
        # Chercher les conversations avec student1, student2, student3
        for student_name in ['student1', 'student2', 'student3']:
            student = db.query(User).filter(User.username == student_name).first()
            if student:
                print(f"\n  {student_name} (ID: {student.id}):")
                
                # Chercher les threads avec ce nom dans le titre
                threads_for_student = db.query(Thread).filter(
                    Thread.title.like(f"%{student_name}%")
                ).all()
                
                for thread in threads_for_student:
                    print(f"    Thread {thread.id}: '{thread.title}'")
                    messages_in_thread = db.query(Message).filter(Message.thread_id == thread.id).count()
                    unread_messages = db.query(Message).filter(
                        Message.thread_id == thread.id,
                        Message.user_id == student.id,
                        Message.is_read == False
                    ).count()
                    print(f"      Messages: {messages_in_thread}, Non lus: {unread_messages}")
            else:
                print(f"  {student_name}: Non trouvé")
        
        print("\n=== RÉSUMÉ ===")
        print(f"✅ {len(users)} utilisateurs dans la base")
        print(f"✅ {len(threads)} conversations/threads")
        print(f"✅ {len(messages)} messages")
        print(f"✅ {len(classes)} classes")
        
        if len(messages) > 0:
            print("✅ Les données de messagerie existent réellement dans la base de données")
        else:
            print("❌ Aucun message trouvé dans la base de données")
            
    except Exception as e:
        print(f"Erreur: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    check_messaging_database() 