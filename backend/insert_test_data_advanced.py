#!/usr/bin/env python3
"""
Script pour insérer des données de test pour les nouvelles fonctionnalités
- Gestion des Devoirs
- Calendrier Avancé
- Collaboration
- IA Avancée
- Rapports Détaillés
"""

import sqlite3
import json
from datetime import datetime, timedelta
from pathlib import Path

def insert_test_data():
    """Insérer des données de test pour toutes les fonctionnalités"""
    
    # Chemin vers la base de données
    db_path = Path(__file__).parent.parent / "data" / "app.db"
    
    if not db_path.exists():
        print(f"❌ Base de données non trouvée: {db_path}")
        return False
    
    print(f"📁 Base de données trouvée: {db_path}")
    
    # Connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier que les utilisateurs existent
        cursor.execute("SELECT id, role FROM users LIMIT 5")
        users = cursor.fetchall()
        
        if not users:
            print("❌ Aucun utilisateur trouvé dans la base de données")
            return False
        
        print(f"✅ {len(users)} utilisateurs trouvés")
        
        # Identifier un professeur et un étudiant
        teacher_id = None
        student_id = None
        
        for user_id, role in users:
            if role == 'teacher' and teacher_id is None:
                teacher_id = user_id
            elif role == 'student' and student_id is None:
                student_id = user_id
        
        if not teacher_id:
            print("⚠️ Aucun professeur trouvé, utilisation du premier utilisateur")
            teacher_id = users[0][0]
        
        if not student_id:
            print("⚠️ Aucun étudiant trouvé, utilisation du deuxième utilisateur")
            student_id = users[1][0] if len(users) > 1 else users[0][0]
        
        print(f"👨‍🏫 Professeur ID: {teacher_id}")
        print(f"👨‍🎓 Étudiant ID: {student_id}")
        
        # 1. Insérer des événements de calendrier
        print("\n📅 Insertion d'événements de calendrier...")
        
        # Événements de cours
        events_data = [
            {
                'title': 'Cours de Mathématiques',
                'description': 'Algèbre linéaire - Chapitre 3',
                'event_type': 'course',
                'start_time': datetime.now() + timedelta(days=1, hours=9),
                'end_time': datetime.now() + timedelta(days=1, hours=11),
                'location': 'Salle A101',
                'subject': 'Mathématiques',
                'color': '#3B82F6',
                'created_by': teacher_id
            },
            {
                'title': 'Examen de Physique',
                'description': 'Examen final - Mécanique',
                'event_type': 'exam',
                'start_time': datetime.now() + timedelta(days=3, hours=14),
                'end_time': datetime.now() + timedelta(days=3, hours=16),
                'location': 'Salle B203',
                'subject': 'Physique',
                'color': '#EF4444',
                'created_by': teacher_id
            },
            {
                'title': 'Session d\'étude - Histoire',
                'description': 'Révision pour l\'examen',
                'event_type': 'study_session',
                'start_time': datetime.now() + timedelta(days=2, hours=15),
                'end_time': datetime.now() + timedelta(days=2, hours=17),
                'location': 'Bibliothèque',
                'subject': 'Histoire',
                'color': '#10B981',
                'created_by': student_id
            }
        ]
        
        for event in events_data:
            cursor.execute("""
                INSERT INTO calendar_events 
                (title, description, event_type, start_time, end_time, location, subject, color, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                event['title'], event['description'], event['event_type'],
                event['start_time'], event['end_time'], event['location'],
                event['subject'], event['color'], event['created_by']
            ))
        
        print(f"✅ {len(events_data)} événements de calendrier créés")
        
        # 2. Insérer des sessions d'étude
        print("\n📚 Insertion de sessions d'étude...")
        
        sessions_data = [
            {
                'title': 'Révision Mathématiques',
                'description': 'Exercices d\'algèbre',
                'subject': 'Mathématiques',
                'start_time': datetime.now() + timedelta(days=1, hours=16),
                'duration': 120,
                'goals': json.dumps(['Comprendre les matrices', 'Résoudre les équations']),
                'student_id': student_id
            },
            {
                'title': 'Préparation Physique',
                'description': 'Résolution de problèmes',
                'subject': 'Physique',
                'start_time': datetime.now() + timedelta(days=2, hours=10),
                'duration': 90,
                'goals': json.dumps(['Maîtriser la cinématique', 'Préparer l\'examen']),
                'student_id': student_id
            }
        ]
        
        for session in sessions_data:
            cursor.execute("""
                INSERT INTO calendar_study_sessions 
                (title, description, subject, start_time, duration, goals, student_id)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                session['title'], session['description'], session['subject'],
                session['start_time'], session['duration'], session['goals'], session['student_id']
            ))
        
        print(f"✅ {len(sessions_data)} sessions d'étude créées")
        
        # 3. Insérer des groupes d'étude
        print("\n👥 Insertion de groupes d'étude...")
        
        groups_data = [
            {
                'name': 'Groupe Mathématiques Avancées',
                'description': 'Groupe d\'étude pour les mathématiques de niveau avancé',
                'subject': 'Mathématiques',
                'max_members': 8,
                'is_public': True,
                'created_by': teacher_id
            },
            {
                'name': 'Équipe Projet Physique',
                'description': 'Collaboration sur le projet de mécanique',
                'subject': 'Physique',
                'max_members': 6,
                'is_public': False,
                'created_by': student_id
            }
        ]
        
        group_ids = []
        for group in groups_data:
            cursor.execute("""
                INSERT INTO study_groups 
                (name, description, subject, max_members, is_public, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                group['name'], group['description'], group['subject'],
                group['max_members'], group['is_public'], group['created_by']
            ))
            group_ids.append(cursor.lastrowid)
        
        print(f"✅ {len(groups_data)} groupes d'étude créés")
        
        # 4. Ajouter des membres aux groupes
        print("\n👤 Ajout de membres aux groupes...")
        
        for group_id in group_ids:
            # Ajouter le créateur comme membre
            cursor.execute("""
                INSERT INTO study_group_members 
                (group_id, user_id, role)
                VALUES (?, ?, 'admin')
            """, (group_id, teacher_id if group_id == group_ids[0] else student_id))
            
            # Ajouter l'autre utilisateur
            other_user = student_id if group_id == group_ids[0] else teacher_id
            cursor.execute("""
                INSERT INTO study_group_members 
                (group_id, user_id, role)
                VALUES (?, ?, 'member')
            """, (group_id, other_user))
        
        print("✅ Membres ajoutés aux groupes")
        
        # 5. Insérer des messages de groupe
        print("\n💬 Insertion de messages de groupe...")
        
        messages_data = [
            {
                'group_id': group_ids[0],
                'user_id': teacher_id,
                'content': 'Bienvenue dans le groupe Mathématiques Avancées !',
                'message_type': 'text'
            },
            {
                'group_id': group_ids[0],
                'user_id': student_id,
                'content': 'Merci ! J\'ai des questions sur les matrices.',
                'message_type': 'text'
            },
            {
                'group_id': group_ids[1],
                'user_id': student_id,
                'content': 'Quelqu\'un veut travailler sur le projet ce weekend ?',
                'message_type': 'text'
            }
        ]
        
        for message in messages_data:
            cursor.execute("""
                INSERT INTO group_messages 
                (group_id, user_id, content, message_type)
                VALUES (?, ?, ?, ?)
            """, (
                message['group_id'], message['user_id'],
                message['content'], message['message_type']
            ))
        
        print(f"✅ {len(messages_data)} messages de groupe créés")
        
        # 6. Insérer des recommandations IA
        print("\n🤖 Insertion de recommandations IA...")
        
        ai_recommendations = [
            {
                'user_id': student_id,
                'recommendation_type': 'content',
                'title': 'Vidéo sur les matrices',
                'description': 'Regardez cette vidéo pour mieux comprendre les matrices',
                'confidence_score': 0.85,
                'reason': 'Basé sur vos difficultés en algèbre'
            },
            {
                'user_id': student_id,
                'recommendation_type': 'quiz',
                'title': 'Quiz de révision Physique',
                'description': 'Testez vos connaissances en mécanique',
                'confidence_score': 0.78,
                'reason': 'Examen dans 3 jours'
            }
        ]
        
        for rec in ai_recommendations:
            cursor.execute("""
                INSERT INTO ai_recommendations 
                (user_id, recommendation_type, title, description, confidence_score, reason)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                rec['user_id'], rec['recommendation_type'], rec['title'],
                rec['description'], rec['confidence_score'], rec['reason']
            ))
        
        print(f"✅ {len(ai_recommendations)} recommandations IA créées")
        
        # 7. Insérer des sessions de tutorat IA
        print("\n🎓 Insertion de sessions de tutorat IA...")
        
        tutoring_sessions = [
            {
                'user_id': student_id,
                'subject': 'Mathématiques',
                'topic': 'Algèbre linéaire',
                'session_type': 'remedial',
                'status': 'completed'
            },
            {
                'user_id': student_id,
                'subject': 'Physique',
                'topic': 'Mécanique',
                'session_type': 'preparation',
                'status': 'active'
            }
        ]
        
        session_ids = []
        for session in tutoring_sessions:
            cursor.execute("""
                INSERT INTO ai_tutoring_sessions 
                (user_id, subject, topic, session_type, status)
                VALUES (?, ?, ?, ?, ?)
            """, (
                session['user_id'], session['subject'], session['topic'],
                session['session_type'], session['status']
            ))
            session_ids.append(cursor.lastrowid)
        
        print(f"✅ {len(tutoring_sessions)} sessions de tutorat IA créées")
        
        # 8. Insérer des interactions de tutorat
        print("\n💭 Insertion d'interactions de tutorat...")
        
        interactions = [
            {
                'session_id': session_ids[0],
                'user_message': 'Je ne comprends pas comment calculer le déterminant d\'une matrice 3x3',
                'ai_response': 'Pour calculer le déterminant d\'une matrice 3x3, vous pouvez utiliser la règle de Sarrus...',
                'interaction_type': 'question',
                'user_satisfaction': 4
            },
            {
                'session_id': session_ids[1],
                'user_message': 'Pouvez-vous m\'expliquer la deuxième loi de Newton ?',
                'ai_response': 'La deuxième loi de Newton dit que la force nette agissant sur un objet est égale à sa masse multipliée par son accélération...',
                'interaction_type': 'explanation',
                'user_satisfaction': 5
            }
        ]
        
        for interaction in interactions:
            cursor.execute("""
                INSERT INTO ai_tutoring_interactions 
                (session_id, user_message, ai_response, interaction_type, user_satisfaction)
                VALUES (?, ?, ?, ?, ?)
            """, (
                interaction['session_id'], interaction['user_message'],
                interaction['ai_response'], interaction['interaction_type'],
                interaction['user_satisfaction']
            ))
        
        print(f"✅ {len(interactions)} interactions de tutorat créées")
        
        # 9. Insérer des détections de difficultés
        print("\n⚠️ Insertion de détections de difficultés...")
        
        difficulties = [
            {
                'user_id': student_id,
                'subject': 'Mathématiques',
                'topic': 'Matrices',
                'difficulty_level': 'high',
                'confidence_score': 0.82,
                'evidence': json.dumps({'quiz_scores': [45, 52, 38], 'time_spent': 'long'})
            },
            {
                'user_id': student_id,
                'subject': 'Physique',
                'topic': 'Cinématique',
                'difficulty_level': 'medium',
                'confidence_score': 0.65,
                'evidence': json.dumps({'quiz_scores': [68, 72], 'time_spent': 'normal'})
            }
        ]
        
        for difficulty in difficulties:
            cursor.execute("""
                INSERT INTO difficulty_detection 
                (user_id, subject, topic, difficulty_level, confidence_score, evidence)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                difficulty['user_id'], difficulty['subject'], difficulty['topic'],
                difficulty['difficulty_level'], difficulty['confidence_score'],
                difficulty['evidence']
            ))
        
        print(f"✅ {len(difficulties)} détections de difficultés créées")
        
        # 10. Insérer des devoirs
        print("\n📝 Insertion de devoirs...")
        
        homework_assignments = [
            {
                'title': 'Exercices de matrices',
                'description': 'Résoudre les exercices 1 à 10 du chapitre 3',
                'subject': 'Mathématiques',
                'class_id': 1,  # Assumons que la classe 1 existe
                'assigned_by': teacher_id,
                'due_date': datetime.now() + timedelta(days=7),
                'max_score': 100,
                'instructions': 'Utilisez la méthode de Gauss pour la résolution'
            },
            {
                'title': 'Problème de mécanique',
                'description': 'Analyser le mouvement d\'un projectile',
                'subject': 'Physique',
                'class_id': 1,
                'assigned_by': teacher_id,
                'due_date': datetime.now() + timedelta(days=5),
                'max_score': 50,
                'instructions': 'Dessinez le diagramme des forces et calculez la trajectoire'
            }
        ]
        
        assignment_ids = []
        for assignment in homework_assignments:
            cursor.execute("""
                INSERT INTO homework_assignments 
                (title, description, subject, class_id, assigned_by, due_date, max_score, instructions)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                assignment['title'], assignment['description'], assignment['subject'],
                assignment['class_id'], assignment['assigned_by'], assignment['due_date'],
                assignment['max_score'], assignment['instructions']
            ))
            assignment_ids.append(cursor.lastrowid)
        
        print(f"✅ {len(homework_assignments)} devoirs créés")
        
        # 11. Insérer des soumissions de devoirs
        print("\n📤 Insertion de soumissions de devoirs...")
        
        submissions = [
            {
                'assignment_id': assignment_ids[0],
                'student_id': student_id,
                'content': 'J\'ai résolu les exercices 1, 2, 3, 5, 7, 9. Les exercices 4, 6, 8, 10 me posent problème.',
                'status': 'submitted'
            },
            {
                'assignment_id': assignment_ids[1],
                'student_id': student_id,
                'content': 'Voici mon analyse du mouvement du projectile avec les calculs.',
                'status': 'submitted'
            }
        ]
        
        for submission in submissions:
            cursor.execute("""
                INSERT INTO homework_submissions 
                (assignment_id, student_id, content, status)
                VALUES (?, ?, ?, ?)
            """, (
                submission['assignment_id'], submission['student_id'],
                submission['content'], submission['status']
            ))
        
        print(f"✅ {len(submissions)} soumissions de devoirs créées")
        
        # 12. Insérer des projets de collaboration
        print("\n🤝 Insertion de projets de collaboration...")
        
        projects = [
            {
                'title': 'Projet de recherche en IA',
                'description': 'Développement d\'un système de recommandation intelligent',
                'subject': 'Informatique',
                'due_date': datetime.now() + timedelta(days=30),
                'status': 'active',
                'created_by': teacher_id
            },
            {
                'title': 'Étude sur les énergies renouvelables',
                'description': 'Analyse comparative des différentes sources d\'énergie',
                'subject': 'Sciences',
                'due_date': datetime.now() + timedelta(days=21),
                'status': 'planning',
                'created_by': student_id
            }
        ]
        
        project_ids = []
        for project in projects:
            cursor.execute("""
                INSERT INTO collaboration_projects 
                (title, description, subject, due_date, status, created_by)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                project['title'], project['description'], project['subject'],
                project['due_date'], project['status'], project['created_by']
            ))
            project_ids.append(cursor.lastrowid)
        
        print(f"✅ {len(projects)} projets de collaboration créés")
        
        # 13. Insérer des tâches de projet
        print("\n✅ Insertion de tâches de projet...")
        
        tasks = [
            {
                'project_id': project_ids[0],
                'title': 'Recherche bibliographique',
                'description': 'Analyser les articles scientifiques sur les systèmes de recommandation',
                'assigned_to': student_id,
                'priority': 'high',
                'status': 'in_progress',
                'due_date': datetime.now() + timedelta(days=7),
                'created_by': teacher_id
            },
            {
                'project_id': project_ids[1],
                'title': 'Collecte de données',
                'description': 'Gather data on renewable energy sources',
                'assigned_to': teacher_id,
                'priority': 'medium',
                'status': 'pending',
                'due_date': datetime.now() + timedelta(days=5),
                'created_by': student_id
            }
        ]
        
        for task in tasks:
            cursor.execute("""
                INSERT INTO project_tasks 
                (project_id, title, description, assigned_to, priority, status, due_date, created_by)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                task['project_id'], task['title'], task['description'],
                task['assigned_to'], task['priority'], task['status'],
                task['due_date'], task['created_by']
            ))
        
        print(f"✅ {len(tasks)} tâches de projet créées")
        
        # 14. Insérer des rapports détaillés
        print("\n📊 Insertion de rapports détaillés...")
        
        reports = [
            {
                'user_id': student_id,
                'report_type': 'performance_analysis',
                'subject': 'Mathématiques',
                'period': 'month',
                'data': json.dumps({
                    'quiz_scores': [75, 82, 68, 79, 85],
                    'time_spent': 12.5,
                    'difficulties': ['Matrices', 'Vecteurs'],
                    'recommendations': ['Plus d\'exercices sur les matrices', 'Révision des bases']
                })
            },
            {
                'user_id': student_id,
                'report_type': 'learning_progress',
                'subject': 'Physique',
                'period': 'week',
                'data': json.dumps({
                    'topics_covered': ['Mécanique', 'Thermodynamique'],
                    'completion_rate': 0.75,
                    'next_topics': ['Ondes', 'Électricité']
                })
            }
        ]
        
        for report in reports:
            cursor.execute("""
                INSERT INTO detailed_reports 
                (user_id, report_type, subject, period, data)
                VALUES (?, ?, ?, ?, ?)
            """, (
                report['user_id'], report['report_type'], report['subject'],
                report['period'], report['data']
            ))
        
        print(f"✅ {len(reports)} rapports détaillés créés")
        
        # Validation finale
        print("\n🔍 Vérification des données insérées...")
        
        # Compter les enregistrements dans chaque table
        tables_to_check = [
            'calendar_events', 'calendar_study_sessions', 'study_groups',
            'group_messages', 'ai_recommendations', 'ai_tutoring_sessions',
            'ai_tutoring_interactions', 'difficulty_detection',
            'homework_assignments', 'homework_submissions',
            'collaboration_projects', 'project_tasks', 'detailed_reports'
        ]
        
        for table in tables_to_check:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]
            print(f"   - {table}: {count} enregistrements")
        
        # Commit des changements
        conn.commit()
        print("\n🎉 Toutes les données de test ont été insérées avec succès!")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'insertion des données: {e}")
        conn.rollback()
        return False
        
    finally:
        conn.close()

if __name__ == "__main__":
    print("🚀 Démarrage de l'insertion des données de test...")
    success = insert_test_data()
    
    if success:
        print("\n✅ Script terminé avec succès!")
    else:
        print("\n❌ Script terminé avec des erreurs!")




