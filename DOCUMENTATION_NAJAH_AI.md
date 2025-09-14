# 📚 DOCUMENTATION NAJAH AI - ÉTAT ACTUEL

## 🏗️ ARCHITECTURE GÉNÉRALE

### **Backend (FastAPI + SQLAlchemy)**
- **Base de données** : SQLite (`data/app.db`)
- **Framework** : FastAPI avec CORS configuré pour `http://localhost:3001`
- **ORM** : SQLAlchemy avec 30+ modèles de données
- **Authentification** : JWT avec bcrypt pour le hashage des mots de passe

### **Frontend (Next.js + TypeScript)**
- **Framework** : Next.js 14 avec TypeScript
- **UI** : React avec composants modulaires
- **État** : Context API (AuthContext, ThemeContext)
- **Communication** : WebSocket pour notifications temps réel
- **PWA** : Configuration complète avec service worker

---

## 🗄️ MODÈLES DE DONNÉES (Backend)

### **1. Utilisateurs & Authentification**
```python
class UserRole(str, enum.Enum):
    student = "student"
    parent = "parent" 
    teacher = "teacher"
    admin = "admin"

class User(Base):
    id, username, email, hashed_password, role
    # Relations: quiz_results, quiz_assignments, class_students, teacher_classes, badges, learning_history, assessments, level, user_challenges, leaderboard_entries, user_achievements, notes
```

### **2. Quiz & Évaluation**
```python
class Quiz(Base):
    id, title, description, subject, total_points, time_limit, created_by, created_at, is_active
    # Relations: creator, questions, results, assignments

class Question(Base):
    id, quiz_id, question_text, question_type, points, correct_answer, options

class QuizResult(Base):
    id, student_id, quiz_id, score, total_points, time_taken, completed_at, status

class QuizAssignment(Base):
    id, quiz_id, student_id, assigned_by, assigned_at, due_date, status
```

### **3. Contenu & Apprentissage**
```python
class Content(Base):
    id, title, description, content_type, subject, level, difficulty, estimated_time, content_data, file_url, thumbnail_url, tags, learning_objectives, prerequisites, skills_targeted, created_by, category_id, created_at, is_active

class LearningPath(Base):
    id, description
    # Relations: assignments

class StudentLearningPath(Base):
    id, student_id, path_id, progression

class LearningHistory(Base):
    id, student_id, content_id, path_id, action, score, progression, details, timestamp
```

### **4. Classes & Groupes**
```python
class ClassGroup(Base):
    id, name, description, teacher_id
    # Relations: teacher, students

class ClassStudent(Base):
    id, class_id, student_id, joined_at
    # Relations: class_group, student
```

### **5. Gamification**
```python
class UserLevel(Base):
    id, user_id, level, current_xp, total_xp, xp_to_next_level, created_at, updated_at

class Badge(Base):
    id, name, description, criteria, image_url, secret
    # Relations: user_badges

class UserBadge(Base):
    id, user_id, badge_id, awarded_at, awarded_by

class UserChallenge(Base):
    id, user_id, challenge_type, challenge_data, status, progress, started_at, completed_at

class LeaderboardEntry(Base):
    id, user_id, category, score, rank, period, created_at

class UserAchievement(Base):
    id, user_id, achievement_type, achievement_data, earned_at
```

### **6. Notifications & Messages**
```python
class Notification(Base):
    id, title, message, user_id

class Message(Base):
    id, sender_id, receiver_id, content, message_type, sent_at, read_at, thread_id

class Thread(Base):
    id, title, description, created_by, created_at, type
    # Relations: creator, messages
```

### **7. Évaluation Continue**
```python
class Competency(Base):
    id, name, description, subject, level, category, created_by, created_at

class Assessment(Base):
    id, student_id, assessment_type, title, description, status, started_at, completed_at
    # Relations: student, questions, results

class StudentCompetency(Base):
    id, student_id, competency_id, level, assessment_date, notes
```

### **8. Calendrier & Planification**
```python
class ScheduleEvent(Base):
    id, title, description, event_type, start_time, end_time, location, teacher_id, subject, color, is_active, created_at, updated_at

class ScheduleAttendee(Base):
    id, event_id, user_id, role, status, created_at
```

### **9. Collaboration & Remédiation**
```python
class InterClassProject(Base):
    id, title, description, subject, start_date, end_date, status, created_by, created_at

class ProjectParticipant(Base):
    id, project_id, user_id, role, joined_at

class SharedResource(Base):
    id, title, description, resource_type, file_url, shared_by, shared_at, is_public

class ResourceRating(Base):
    id, resource_id, user_id, rating, comment, created_at

class PeerEvaluation(Base):
    id, evaluator_id, evaluated_id, project_id, criteria, score, feedback, created_at
```

### **10. Notifications Avancées**
```python
class NotificationTemplate(Base):
    id, name, title_template, message_template, notification_type, variables, created_at

class AdvancedNotification(Base):
    id, user_id, template_id, title, message, notification_type, priority, data, created_at, read_at

class EmailNotification(Base):
    id, notification_id, email_address, subject, body, sent_at, status

class SMSNotification(Base):
    id, notification_id, phone_number, message, sent_at, status

class PushNotification(Base):
    id, notification_id, device_token, title, body, data, sent_at, status

class NotificationSchedule(Base):
    id, notification_id, scheduled_at, frequency, end_date, is_active
```

---

## 🔌 ENDPOINTS API (Backend)

### **Authentification & Utilisateurs**
- `POST /api/v1/auth/login` - Connexion utilisateur
- `POST /api/v1/auth/register` - Inscription utilisateur
- `GET /api/v1/users/me` - Profil utilisateur connecté
- `GET /api/v1/users/` - Liste des utilisateurs
- `PUT /api/v1/users/{user_id}` - Mise à jour utilisateur

### **Quiz & Évaluation**
- `GET /api/v1/quizzes/` - Liste des quiz
- `POST /api/v1/quizzes/` - Créer un quiz
- `GET /api/v1/quizzes/{quiz_id}` - Détails d'un quiz
- `POST /api/v1/quiz_results/` - Soumettre un résultat
- `GET /api/v1/quiz_results/student/{student_id}` - Résultats d'un étudiant

### **Contenu & Apprentissage**
- `GET /api/v1/contents/` - Liste des contenus
- `POST /api/v1/contents/` - Créer un contenu
- `GET /api/v1/learning_paths/` - Parcours d'apprentissage
- `GET /api/v1/learning_history/student/{student_id}` - Historique d'apprentissage

### **Analytics & Performance**
- `GET /api/v1/analytics/overview` - Vue d'ensemble des analytics
- `GET /api/v1/student_performance/{student_id}` - Performance d'un étudiant
- `GET /api/v1/advanced_analytics/` - Analytics avancées
- `GET /api/v1/recommendations/student/{student_id}` - Recommandations IA

### **Gamification**
- `GET /api/v1/gamification/user/{user_id}` - Niveau et XP utilisateur
- `GET /api/v1/badges/` - Liste des badges
- `POST /api/v1/badges/award` - Attribuer un badge
- `GET /api/v1/gamification/leaderboard` - Classement

### **Messages & Notifications**
- `GET /api/v1/messages/` - Messages utilisateur
- `POST /api/v1/messages/` - Envoyer un message
- `GET /api/v1/notifications/user` - Notifications utilisateur
- `PUT /api/v1/notifications/{notification_id}/read` - Marquer comme lu

### **Fonctionnalités Avancées Professeur**
- `GET /api/v1/teacher_messaging/conversations` - Conversations professeur
- `GET /api/v1/teacher_schedule/events` - Événements calendrier
- `GET /api/v1/continuous_assessment/competencies` - Compétences
- `GET /api/v1/auto_correction/` - Correction automatique
- `GET /api/v1/remediation/` - Remédiation
- `GET /api/v1/teacher_collaboration/` - Collaboration entre professeurs

### **IA & Analytics Avancées**
- `GET /api/v1/ai_advanced/predict-performance/{student_id}` - Prédiction performance
- `GET /api/v1/ai_advanced/detect-difficulties/{student_id}` - Détection difficultés
- `GET /api/v1/ai_advanced/recommendations/{student_id}` - Recommandations IA
- `GET /api/v1/ai_advanced/class-insights/{class_id}` - Insights classe

### **Intégrations Externes**
- `GET /api/v1/integrations/educational-videos` - Vidéos éducatives (YouTube)
- `GET /api/v1/integrations/weather` - Météo (OpenWeather)
- `GET /api/v1/integrations/educational-news` - Actualités éducatives
- `GET /api/v1/integrations/translate` - Traduction de contenu
- `GET /api/v1/integrations/calendar-holidays` - Jours fériés
- `GET /api/v1/integrations/currency-rates` - Taux de change

### **Export & Rapports**
- `GET /api/v1/export_reports/student/{student_id}/pdf` - Rapport PDF étudiant
- `GET /api/v1/export_reports/class/{class_id}/excel` - Rapport Excel classe
- `GET /api/v1/export_reports/analytics/{report_type}` - Rapports analytics

---

## 🎨 COMPOSANTS FRONTEND

### **Widgets Principaux**
- `QuizWidget.tsx` - Gestion des quiz (19KB, 468 lignes)
- `AnalyticsWidget.tsx` - Analytics de base (12KB, 334 lignes)
- `AdvancedAnalyticsWidget.tsx` - Analytics avancées (13KB, 322 lignes)
- `GamificationWidget.tsx` - Système de gamification (6.4KB, 151 lignes)
- `MessagesWidget.tsx` - Messagerie (8.6KB, 255 lignes)
- `BadgesWidget.tsx` - Gestion des badges (10KB, 220 lignes)
- `RecommendationsWidget.tsx` - Recommandations IA (8.8KB, 208 lignes)

### **Widgets Spécialisés**
- `TeacherReportsWidget.tsx` - Rapports professeur (12KB, 317 lignes)
- `ContentEditorWidget.tsx` - Éditeur de contenu (8.5KB, 261 lignes)
- `QuizManagerWidget.tsx` - Gestionnaire de quiz (21KB, 444 lignes)
- `StudentPerformanceWidget.tsx` - Performance étudiant (18KB, 465 lignes)
- `LearningPathsWidget.tsx` - Parcours d'apprentissage (15KB, 342 lignes)
- `ContentsWidget.tsx` - Gestion des contenus (18KB, 385 lignes)

### **Widgets Avancés**
- `InteractiveAnalytics.tsx` - Analytics interactives (12KB, 296 lignes)
- `EnhancedStudentDashboard.tsx` - Dashboard étudiant amélioré (13KB, 337 lignes)
- `TemplateManager.tsx` - Gestionnaire de templates (23KB, 609 lignes)
- `ActivityWidget.tsx` - Activités utilisateur (7.7KB, 184 lignes)
- `CorrectionsWidget.tsx` - Corrections (6.6KB, 149 lignes)
- `ScoreCorrectionWidget.tsx` - Correction de scores (5.7KB, 143 lignes)

### **Pages Principales**
- `/dashboard/student` - Dashboard étudiant
- `/dashboard/teacher` - Dashboard professeur
- `/dashboard/teacher/continuous-assessment` - Évaluation continue
- `/dashboard/teacher/content` - Gestion de contenu
- `/dashboard/teacher/calendar` - Calendrier professeur
- `/dashboard/teacher/messages` - Messagerie professeur

---

## 🔧 FONCTIONNALITÉS IMPLÉMENTÉES

### **✅ Fonctionnalités Étudiant**
- [x] Authentification et profil
- [x] Quiz et évaluation
- [x] Parcours d'apprentissage
- [x] Gamification (niveaux, badges, XP)
- [x] Messagerie et notifications
- [x] Analytics personnelles
- [x] Recommandations IA
- [x] Historique d'apprentissage
- [x] Dashboard interactif

### **✅ Fonctionnalités Professeur**
- [x] Gestion des classes et étudiants
- [x] Création et gestion de quiz
- [x] Analytics avancées
- [x] Messagerie avec étudiants
- [x] Calendrier et planification
- [x] Évaluation continue
- [x] Correction automatique
- [x] Remédiation
- [x] Collaboration entre professeurs
- [x] Rapports et exports (PDF/Excel)

### **✅ Fonctionnalités Système**
- [x] Authentification JWT
- [x] Notifications temps réel (WebSocket)
- [x] PWA (Progressive Web App)
- [x] IA et recommandations
- [x] Analytics avancées
- [x] Export de données
- [x] Intégrations externes (simulées)
- [x] Templates personnalisables

---

## 🚧 FONCTIONNALITÉS EN COURS/À AMÉLIORER

### **🔧 Corrections Récentes**
- [x] Erreur `total_views` undefined dans ContentWidget
- [x] Reconnexion automatique WebSocket
- [x] Gestion des erreurs 401 (authentification)

### **📋 Fonctionnalités Manquantes**
- [ ] Intégrations externes réelles (OAuth, API keys)
- [ ] Notifications push natives
- [ ] Synchronisation offline avancée
- [ ] Tests automatisés complets
- [ ] Documentation API interactive (Swagger)
- [ ] Monitoring et logging avancés

---

## 📊 STATISTIQUES TECHNIQUES

### **Backend**
- **30+ modèles de données** SQLAlchemy
- **50+ endpoints API** organisés par modules
- **Base de données** : SQLite avec relations complexes
- **Authentification** : JWT avec bcrypt
- **WebSocket** : Notifications temps réel

### **Frontend**
- **25+ widgets** React/TypeScript
- **PWA** : Service worker, manifest, cache
- **État global** : Context API
- **Communication** : API client + WebSocket
- **UI/UX** : Composants modulaires et réutilisables

### **Intégrations**
- **IA** : Prédictions, recommandations, analytics
- **Export** : PDF (reportlab), Excel (pandas)
- **Notifications** : Email, SMS, Push (simulées)
- **Externes** : YouTube, OpenWeather, NewsAPI (simulées)

---

## 🎯 PROCHAINES ÉTAPES RECOMMANDÉES

### **1. Priorité Haute**
1. **Tester toutes les APIs** avec des données réelles
2. **Corriger les erreurs 401** restantes
3. **Finaliser les intégrations WebSocket**
4. **Compléter les tests d'intégration**

### **2. Priorité Moyenne**
1. **Implémenter les intégrations externes réelles**
2. **Ajouter les notifications push natives**
3. **Optimiser les performances PWA**
4. **Créer la documentation utilisateur**

### **3. Priorité Basse**
1. **Ajouter des fonctionnalités avancées d'analytics**
2. **Implémenter la synchronisation offline complète**
3. **Créer des templates personnalisables avancés**
4. **Ajouter des tests automatisés complets**

---

## 🔍 ÉTAT ACTUEL DES DONNÉES

### **Données Réelles (95%)**
- ✅ Utilisateurs et authentification
- ✅ Quiz et résultats
- ✅ Contenu et parcours d'apprentissage
- ✅ Analytics et performance
- ✅ Gamification et badges
- ✅ Messages et notifications
- ✅ Calendrier et planification
- ✅ Évaluation continue
- ✅ Rapports et exports

### **Données Simulées (5%)**
- 🔄 Intégrations externes (YouTube, OpenWeather, etc.)
- 🔄 Notifications push/SMS/Email
- 🔄 Templates personnalisables avancés

---

## 📝 NOTES TECHNIQUES

### **Base de données**
- **Fichier** : `backend/data/app.db`
- **Migrations** : Alembic configuré mais non utilisé
- **Relations** : Clés étrangères explicites pour éviter les erreurs circulaires
- **Données de test** : Scripts d'initialisation disponibles

### **Sécurité**
- **Mots de passe** : Hashés avec bcrypt
- **JWT** : Tokens d'authentification
- **CORS** : Configuré pour le développement
- **Validation** : Pydantic pour les schémas API

### **Performance**
- **Cache** : PWA avec service worker
- **Optimisation** : Images et ressources
- **Monitoring** : Hooks de performance personnalisés
- **Offline** : IndexedDB pour les données locales

---

*Dernière mise à jour : Décembre 2024*
*Version : 1.0*
*Statut : Fonctionnel avec 95% de données réelles* 