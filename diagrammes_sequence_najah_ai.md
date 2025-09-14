# Diagrammes de Séquence - Projet Najah AI

## 1. Diagramme de Séquence - ÉTUDIANT

```mermaid
sequenceDiagram
    participant S as Student
    participant F as Frontend
    participant B as Backend
    participant DB as Database
    participant AI as AI Services

    Note over S,AI: Connexion et Authentification
    S->>F: Se connecte avec email/password
    F->>B: POST /auth/login
    B->>DB: Vérifier credentials
    DB-->>B: User data + role
    B->>B: Générer JWT token
    B-->>F: JWT token + user info
    F->>F: Stocker token
    F-->>S: Afficher dashboard étudiant

    Note over S,AI: Évaluation Initiale
    S->>F: Commence évaluation initiale
    F->>B: GET /assessments/initial
    B->>AI: Récupérer questions adaptatives
    AI-->>B: Questions pool adaptatives
    B->>AI: Analyser niveau initial
    AI-->>B: Niveau estimé + questions
    B-->>F: Questions adaptées
    F-->>S: Afficher questions

    Note over S,AI: Réponses et Adaptation
    S->>F: Répond aux questions
    F->>B: POST /assessments/{id}/submit
    B->>AI: Analyser réponses
    AI->>AI: Calculer score + difficulté
    AI-->>B: Analyse + recommandations
    B->>DB: Sauvegarder résultats
    B->>AI: Générer parcours adaptatif
    AI-->>B: Parcours personnalisé
    B-->>F: Nouveau parcours + feedback
    F-->>S: Afficher progression

    Note over S,AI: Apprentissage Continu
    S->>F: Accède au parcours d'apprentissage
    F->>B: GET /learning-paths/{id}
    B->>AI: Récupérer parcours adaptatif
    AI-->>B: Learning path data adaptatif
    B->>AI: Analyser progression
    AI-->>B: Recommandations + adaptation
    B-->>F: Contenu adapté
    F-->>S: Afficher contenu

    Note over S,AI: Suivi de Progression
    S->>F: Interagit avec contenu
    F->>B: POST /progress/track
    B->>DB: Sauvegarder activité
    B->>AI: Analyser patterns
    AI-->>B: Insights + alertes
    B->>DB: Mettre à jour analytics
    B-->>F: Feedback en temps réel
    F-->>S: Afficher feedback

    Note over S,AI: Collaboration
    S->>F: Rejoint groupe d'étude
    F->>B: POST /collaboration/study-groups/{id}/join
    B->>DB: Mettre à jour groupe
    B-->>F: Confirmer adhésion
    F-->>S: Groupe rejoint

    S->>F: Partage ressource
    F->>B: POST /collaboration/study-groups/{id}/resources
    B->>DB: Sauvegarder ressource
    B-->>F: Ressource partagée
    F-->>S: Confirmer partage

    Note over S,AI: Planification
    S->>F: Planifie session d'étude
    F->>B: POST /calendar/study-sessions
    B->>DB: Créer session
    DB-->>B: Session créée
    B-->>F: Session planifiée
    F-->>S: Confirmer planification

    Note over S,AI: Soumission Devoir
    S->>F: Soumet devoir
    F->>B: POST /homework/{id}/submit
    B->>DB: Sauvegarder soumission
    B->>B: Calculer score automatique
    B-->>F: Devoir soumis + score
    F-->>S: Confirmer soumission
```

## 2. Diagramme de Séquence - ENSEIGNANT

```mermaid
sequenceDiagram
    participant T as Teacher
    participant F as Frontend
    participant B as Backend _
    participant DB as Database
    participant AI as AI Services
    participant S as Student

    Note over T,AI: Connexion et Authentification
    T->>F: Se connecte avec email/password
    F->>B: POST /auth/login
    B->>DB: Vérifier credentials
    DB-->>B: User data + role teacher
    B->>B: Générer JWT token
    B-->>F: JWT token + user info
    F->>F: Stocker token
    F-->>T: Afficher dashboard enseignant

    Note over T,AI: Gestion des Classes
    T->>F: Consulte ses classes
    F->>B: GET /teacher/classes
    B->>DB: Récupérer classes du professeur
    DB-->>B: Classes data
    B-->>F: Liste des classes
    F-->>T: Afficher classes

    T->>F: Crée nouvelle classe
    F->>B: POST /teacher/classes
    B->>DB: Créer classe
    DB-->>B: Classe créée
    B-->>F: Classe créée
    F-->>T: Confirmer création

    Note over T,AI: Création d'Évaluations
    T->>F: Crée évaluation
    F->>B: POST /teacher/assessments
    B->>B: Valider données évaluation
    B->>DB: Créer évaluation
    DB-->>B: Évaluation créée
    B->>AI: Générer questions par IA
    AI-->>B: Questions générées
    B->>DB: Sauvegarder questions
    B-->>F: Évaluation créée
    F-->>T: Confirmer création

    Note over T,AI: Suivi des Élèves
    T->>F: Consulte performance classe
    F->>B: GET /teacher/classes/{id}/analytics
    B->>DB: Récupérer données classe
    DB-->>B: Performance data
    B->>AI: Analyser performances
    AI-->>B: Insights + recommandations
    B-->>F: Analytics complets
    F-->>T: Afficher analytics

    T->>F: Consulte élève spécifique
    F->>B: GET /teacher/students/{id}/progress
    B->>DB: Récupérer données élève
    DB-->>B: Student progress data
    B->>AI: Analyser progression élève
    AI-->>B: Analyse détaillée
    B-->>F: Progression élève
    F-->>T: Afficher progression

    Note over T,AI: Communication
    T->>F: Envoie message à élève
    F->>B: POST /teacher/communication/messages
    B->>DB: Sauvegarder message
    B->>F: Envoyer notification
    F-->>S: Notification reçue
    B-->>F: Message envoyé
    F-->>T: Confirmer envoi

    T->>F: Envoie message aux parents
    F->>B: POST /teacher/communication/parent-messages
    B->>DB: Sauvegarder message parent
    B-->>F: Message envoyé
    F-->>T: Confirmer envoi

    Note over T,AI: Création de Contenu
    T->>F: Crée contenu pédagogique
    F->>B: POST /teacher/content
    B->>B: Valider contenu
    B->>DB: Sauvegarder contenu
    DB-->>B: Contenu créé
    B-->>F: Contenu créé
    F-->>T: Confirmer création

    Note over T,AI: Génération de Rapports
    T->>F: Génère rapport classe
    F->>B: POST /teacher/reports/generate
    B->>DB: Récupérer données complètes
    DB-->>B: Complete class data
    B->>AI: Analyser données
    AI-->>B: Insights + prédictions
    B->>B: Générer rapport PDF
    B-->>F: Rapport généré
    F-->>T: Télécharger rapport

    Note over T,AI: Remédiation
    T->>F: Consulte alertes difficultés
    F->>B: GET /teacher/alerts
    B->>DB: Récupérer alertes
    DB-->>B: Alerts data
    B-->>F: Alertes
    F-->>T: Afficher alertes

    T->>F: Crée plan de remédiation
    F->>B: POST /teacher/remediation/plans
    B->>AI: Générer plan personnalisé
    AI-->>B: Plan de remédiation
    B->>DB: Sauvegarder plan
    B-->>F: Plan créé
    F-->>T: Confirmer création

    Note over T,AI: Notation et Feedback
    T->>F: Note soumission élève
    F->>B: PUT /teacher/homework/submissions/{id}/grade
    B->>DB: Sauvegarder note
    B->>AI: Analyser feedback
    AI-->>B: Suggestions feedback
    B->>DB: Sauvegarder feedback
    B-->>F: Note + feedback sauvegardés
    F-->>T: Confirmer notation
```

## Utilisation

Ces codes Mermaid peuvent être utilisés dans :
- GitHub (dans les fichiers .md)
- GitLab
- Notion
- Obsidian
- Tout éditeur supportant Mermaid

## Fonctionnalités couvertes

### Diagramme Étudiant :
- Connexion et authentification
- Évaluation initiale adaptative
- Apprentissage continu avec IA
- Suivi de progression
- Collaboration et groupes d'étude
- Planification de sessions
- Soumission de devoirs

### Diagramme Enseignant :
- Connexion et authentification
- Gestion des classes
- Création d'évaluations avec IA
- Suivi des performances élèves
- Communication avec élèves et parents
- Création de contenu pédagogique
- Génération de rapports
- Remédiation et alertes
- Notation et feedback
