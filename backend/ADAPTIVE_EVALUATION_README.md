# 🧠 SYSTÈME D'ÉVALUATION ADAPTATIVE - NAJAH AI

## 📋 Vue d'ensemble

Le système d'évaluation adaptative de Najah AI permet aux enseignants de créer, assigner et suivre des tests qui s'adaptent automatiquement au niveau de chaque étudiant en temps réel.

## 🚀 Fonctionnalités Implémentées

### ✅ **Phase 1 : Infrastructure de Base**
- Tables de base de données complètes
- Modèles SQLAlchemy
- Système d'authentification et autorisation

### ✅ **Phase 2 : Endpoints API Complets**
- Création de tests adaptatifs
- Assignation aux classes/étudiants
- Suivi des performances en temps réel
- Analytics détaillés

## 🗄️ Structure de la Base de Données

### Tables Principales

#### `adaptive_tests`
```sql
- id: Identifiant unique
- title: Titre du test
- subject: Matière
- description: Description détaillée
- difficulty_range: Plage de difficulté (JSON)
- question_pool_size: Taille de la banque de questions
- adaptation_algorithm: Algorithme d'adaptation (irt/ml/expert)
- is_active: Statut actif/inactif
- created_by: ID de l'enseignant créateur
- created_at: Date de création
- updated_at: Date de mise à jour
```

#### `adaptive_questions`
```sql
- id: Identifiant unique
- test_id: Référence au test
- question_text: Texte de la question
- question_type: Type (multiple_choice, true_false, fill_blank, essay)
- options: Options pour les questions à choix multiples (JSON)
- correct_answer: Réponse correcte
- explanation: Explication de la réponse
- difficulty_level: Niveau de difficulté (1-10)
- subject: Matière
- topic: Sujet spécifique
- tags: Tags de classification (JSON)
```

#### `test_assignments`
```sql
- id: Identifiant unique
- test_id: Référence au test
- assignment_type: Type d'assignation (class/student/individual)
- target_id: ID de la classe ou de l'étudiant
- assigned_by: ID de l'enseignant qui assigne
- assigned_at: Date d'assignation
- due_date: Date limite
- is_active: Statut actif
- notification_sent: Notification envoyée
```

#### `adaptive_test_performance`
```sql
- id: Identifiant unique
- test_id: Référence au test
- student_id: Référence à l'étudiant
- class_id: Référence à la classe
- start_time: Heure de début
- completion_time: Heure de fin
- total_questions: Nombre total de questions
- questions_answered: Questions répondues
- correct_answers: Réponses correctes
- final_score: Score final
- initial_difficulty_level: Niveau initial
- final_difficulty_level: Niveau final
- difficulty_adjustments: Nombre d'ajustements
- average_response_time: Temps de réponse moyen
- confidence_levels_avg: Niveau de confiance moyen
- learning_patterns: Patterns d'apprentissage (JSON)
- recommendations: Recommandations (JSON)
- status: Statut (not_started/in_progress/completed/abandoned)
```

## 🔌 Endpoints API

### Endpoints Enseignants

#### **Création de Tests**
```http
POST /api/v1/teacher-adaptive-evaluation/tests/create
```
**Corps de la requête :**
```json
{
  "title": "Test de Mathématiques - Équations",
  "subject": "Mathématiques",
  "description": "Test adaptatif sur les équations",
  "difficulty_range": {"min": 3, "max": 8},
  "question_pool_size": 20,
  "adaptation_algorithm": "irt",
  "is_active": true,
  "questions": [
    {
      "question_text": "Résoudre 2x + 5 = 13",
      "question_type": "multiple_choice",
      "options": ["x = 4", "x = 5", "x = 6", "x = 7"],
      "correct_answer": "x = 4",
      "explanation": "2x + 5 = 13 → 2x = 8 → x = 4",
      "difficulty_level": 3
    }
  ]
}
```

#### **Assignation de Tests**
```http
POST /api/v1/teacher-adaptive-evaluation/tests/{test_id}/assign
```
**Corps de la requête :**
```json
{
  "class_ids": [1, 2],
  "student_ids": [4, 5, 6],
  "due_date": "2024-02-15T23:59:59Z"
}
```

#### **Récupération des Tests de l'Enseignant**
```http
GET /api/v1/teacher-adaptive-evaluation/tests/teacher/{teacher_id}
```

#### **Résultats Détaillés d'un Test**
```http
GET /api/v1/teacher-adaptive-evaluation/tests/{test_id}/results
```

#### **Analytics d'une Classe**
```http
GET /api/v1/teacher-adaptive-evaluation/analytics/class/{class_id}
```

#### **Dashboard Enseignant**
```http
GET /api/v1/teacher-adaptive-evaluation/dashboard/overview
```

### Endpoints Étudiants

#### **Tests Disponibles**
```http
GET /api/v1/adaptive-evaluation/tests
```

#### **Démarrer un Test**
```http
POST /api/v1/adaptive-evaluation/tests/{test_id}/start
```

#### **Soumettre une Réponse**
```http
POST /api/v1/adaptive-evaluation/tests/{test_id}/answer
```
**Corps de la requête :**
```json
{
  "question_id": 123,
  "answer": "x = 4",
  "response_time": 15.5,
  "confidence_level": 4
}
```

#### **Terminer un Test**
```http
POST /api/v1/adaptive-evaluation/tests/{test_id}/complete
```

## 🧮 Algorithmes d'Adaptation

### 1. **IRT (Item Response Theory)**
- Estimation de la capacité de l'étudiant
- Sélection de questions optimales
- Ajustement de la difficulté en temps réel

### 2. **Machine Learning (Prévu)**
- Analyse des patterns d'apprentissage
- Prédiction des performances
- Recommandations personnalisées

### 3. **Système Expert**
- Règles métier éducatives
- Adaptation basée sur les compétences
- Stratégies de remédiation

## 📊 Analytics et Rapports

### Métriques Disponibles
- **Performance individuelle** : Score, temps, ajustements
- **Performance de classe** : Moyennes, tendances, comparaisons
- **Analyse des questions** : Taux de réussite, difficulté
- **Patterns d'apprentissage** : Forces, faiblesses, recommandations

### Visualisations
- Graphiques de progression
- Heatmaps de difficulté
- Comparaisons inter-classes
- Tendances temporelles

## 🔧 Configuration et Déploiement

### Prérequis
- Python 3.8+
- SQLite ou PostgreSQL
- FastAPI
- SQLAlchemy

### Installation
```bash
# 1. Créer les tables
python create_adaptive_evaluation_tables.py

# 2. Démarrer le serveur
uvicorn app:fastapi_app --reload --host 0.0.0.0 --port 8000

# 3. Tester les endpoints
python test_adaptive_evaluation_endpoints.py
```

### Variables d'Environnement
```bash
DATABASE_URL=sqlite:///./data/app.db
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## 🧪 Tests et Validation

### Scripts de Test
- `test_adaptive_evaluation_endpoints.py` : Test des endpoints
- `create_adaptive_evaluation_tables.py` : Création des tables

### Données de Test
- Tests d'exemple avec questions
- Assignations de démonstration
- Métriques simulées

## 📈 Roadmap et Évolutions

### **Phase 3 : Intelligence Artificielle Avancée**
- [ ] Algorithmes ML pour l'adaptation
- [ ] Analyse prédictive des performances
- [ ] Génération automatique de questions
- [ ] Détection des blocages d'apprentissage

### **Phase 4 : Intégrations Avancées**
- [ ] LMS (Learning Management System)
- [ ] Outils de création de contenu
- [ ] API tierces (OpenAI, etc.)
- [ ] Export de données (PDF, Excel)

### **Phase 5 : Optimisations**
- [ ] Cache Redis pour les performances
- [ ] Base de données distribuée
- [ ] API GraphQL
- [ ] WebSockets pour le temps réel

## 🐛 Dépannage

### Problèmes Courants

#### **Erreur 404 - Endpoint non trouvé**
- Vérifier que le serveur est démarré
- Contrôler les routes dans `app.py`
- Vérifier les préfixes des routers

#### **Erreur 401 - Non authentifié**
- Vérifier le token JWT
- Contrôler l'expiration du token
- Vérifier les permissions utilisateur

#### **Erreur 500 - Erreur serveur**
- Vérifier les logs du serveur
- Contrôler la connexion à la base de données
- Vérifier les modèles SQLAlchemy

### Logs et Debug
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Dans vos endpoints
logger.debug(f"Données reçues: {data}")
logger.info(f"Test créé avec l'ID: {test_id}")
logger.error(f"Erreur lors de la création: {str(e)}")
```

## 📚 Ressources et Documentation

### Liens Utiles
- [Documentation FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Théorie de Réponse aux Items](https://en.wikipedia.org/wiki/Item_response_theory)

### Support
- Issues GitHub : [Repository Najah AI](https://github.com/your-repo)
- Documentation technique : [Wiki du projet](https://github.com/your-repo/wiki)
- Contact : [Email de support](mailto:support@najah-ai.com)

---

**Version :** 1.0.0  
**Dernière mise à jour :** Janvier 2024  
**Auteur :** Équipe Najah AI  
**Licence :** MIT
























