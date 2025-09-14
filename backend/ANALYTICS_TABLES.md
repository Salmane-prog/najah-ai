# 📊 Tables Analytics - Documentation

## 🎯 **Objectif**
Ces tables sont dédiées exclusivement aux **analytics et prédictions IA** de votre système Najah__AI.

## 🗄️ **Structure des Tables**

### **1. Table `analytics_quizzes`**
**Contenu :** Tous les tests/évaluations créés pour les analytics

```sql
CREATE TABLE analytics_quizzes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- ID unique du test
    title TEXT NOT NULL,                        -- Titre du test
    subject TEXT NOT NULL,                      -- Matière (Français, Histoire, etc.)
    difficulty_level INTEGER CHECK (1-10),      -- Niveau de difficulté
    created_at TIMESTAMP,                       -- Date de création
    updated_at TIMESTAMP                        -- Date de modification
)
```

**Exemples de données :**
- "Test de Grammaire Française - Niveau Intermédiaire" | Français | 6
- "Évaluation Vocabulaire - Thème Commerce" | Français | 5
- "Test de Culture Générale - France Moderne" | Histoire | 6
- "Quiz Mathématiques - Algèbre" | Mathématiques | 7

---

### **2. Table `analytics_results`**
**Contenu :** Tous les résultats obtenus par les étudiants

```sql
CREATE TABLE analytics_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- ID unique du résultat
    user_id INTEGER NOT NULL,                   -- ID de l'étudiant
    quiz_id INTEGER NOT NULL,                   -- ID du test passé
    score REAL NOT NULL CHECK (0-100),          -- Score obtenu (0-100%)
    time_spent INTEGER,                         -- Temps passé (minutes)
    created_at TIMESTAMP                        -- Date/heure du test
)
```

**Exemples de données :**
- Étudiant 15 | Test 1 | 87.5% | 25 min | 2025-01-19 14:30:00
- Étudiant 16 | Test 1 | 92.0% | 30 min | 2025-01-19 15:15:00
- Étudiant 17 | Test 2 | 78.0% | 20 min | 2025-01-19 16:00:00

---

### **3. Table `class_groups`**
**Contenu :** Groupes de classe pour les analytics par classe

```sql
CREATE TABLE class_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,        -- ID unique du groupe
    class_id INTEGER NOT NULL,                  -- ID de la classe
    student_id INTEGER NOT NULL,                -- ID de l'étudiant
    created_at TIMESTAMP                        -- Date d'ajout au groupe
)
```

---

## 🔗 **Relations entre Tables**

```
users (étudiants)
    ↓ (1 étudiant peut passer plusieurs tests)
analytics_results (résultats)
    ↓ (chaque résultat correspond à 1 test)
analytics_quizzes (tests)
```

---

## ⚡ **Index de Performance**

```sql
-- Index pour analytics_results
CREATE INDEX idx_analytics_results_user_id ON analytics_results(user_id)
CREATE INDEX idx_analytics_results_quiz_id ON analytics_results(quiz_id)
CREATE INDEX idx_analytics_results_created_at ON analytics_results(created_at)

-- Index pour analytics_quizzes
CREATE INDEX idx_analytics_quizzes_subject ON analytics_quizzes(subject)
CREATE INDEX idx_analytics_quizzes_difficulty ON analytics_quizzes(difficulty_level)
```

---

## 🎯 **Utilisation dans les Analytics**

### **1. Prédictions IA par étudiant**
```sql
SELECT score, created_at 
FROM analytics_results 
WHERE user_id = ? 
ORDER BY created_at DESC
```

### **2. Performance par matière**
```sql
SELECT AVG(qr.score), q.subject
FROM analytics_results qr
JOIN analytics_quizzes q ON qr.quiz_id = q.id
GROUP BY q.subject
```

### **3. Progrès temporel**
```sql
SELECT strftime('%W', created_at) as week, AVG(score)
FROM analytics_results
GROUP BY week
ORDER BY week
```

---

## 🚀 **Avantages de cette Structure**

1. **Séparation claire** : Tables analytics distinctes des tables métier
2. **Performance optimisée** : Index dédiés aux requêtes analytics
3. **Flexibilité** : Supporte tous types de tests et matières
4. **Traçabilité** : Historique complet des performances
5. **Évolutivité** : Facile d'ajouter de nouveaux champs

---

## 🔧 **Maintenance**

### **Nettoyage automatique**
- Les anciens résultats peuvent être archivés après X mois
- Les tests inactifs peuvent être marqués comme désactivés

### **Sauvegarde**
- Sauvegarde quotidienne des tables analytics
- Export des données pour analyse externe

---

## 📈 **Métriques Calculées**

- **Score moyen global** : Moyenne de tous les scores
- **Taux de completion** : % de tests terminés avec succès
- **Tests difficiles** : % de tests niveau 7+
- **Engagement étudiants** : % d'étudiants actifs récemment
- **Progrès hebdomadaire** : Évolution des scores par semaine
- **Statistiques mensuelles** : Tendances sur 6 mois

---

## 🎉 **Conclusion**

Ces tables constituent le **cœur de votre système d'analytics intelligent** et permettent :
- **Prédictions IA** précises basées sur de vraies données
- **Alertes intelligentes** en temps réel
- **Analytics avancées** pour la prise de décision pédagogique
- **Suivi personnalisé** de chaque étudiant

**Votre système est maintenant prêt pour des analytics de niveau professionnel !** 🚀✨














