-- Script de correction du schéma de base de données
-- À exécuter manuellement dans SQLite

-- 1. Ajouter la colonne 'criteria' manquante dans la table badges
ALTER TABLE badges ADD COLUMN criteria TEXT;

-- 2. Ajouter la colonne 'created_at' manquante dans la table quiz_results
ALTER TABLE quiz_results ADD COLUMN created_at DATETIME DEFAULT CURRENT_TIMESTAMP;

-- 3. Créer la table categories manquante
CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR NOT NULL UNIQUE,
    description TEXT
);

-- 4. Insérer quelques catégories par défaut
INSERT OR IGNORE INTO categories (name, description) VALUES 
('Mathématiques', 'Cours et exercices de mathématiques'),
('Français', 'Cours et exercices de français'),
('Histoire', 'Cours et exercices d''histoire'),
('Géographie', 'Cours et exercices de géographie'),
('Sciences', 'Cours et exercices de sciences');

-- 5. Vérifier que toutes les colonnes nécessaires existent dans quiz_results
-- (Ces colonnes peuvent déjà exister, mais on s'assure qu'elles sont là)
ALTER TABLE quiz_results ADD COLUMN quiz_id INTEGER REFERENCES quizzes(id);
ALTER TABLE quiz_results ADD COLUMN student_id INTEGER REFERENCES users(id);
ALTER TABLE quiz_results ADD COLUMN max_score REAL;
ALTER TABLE quiz_results ADD COLUMN percentage REAL;
ALTER TABLE quiz_results ADD COLUMN started_at DATETIME;
ALTER TABLE quiz_results ADD COLUMN completed_at DATETIME;
ALTER TABLE quiz_results ADD COLUMN is_completed BOOLEAN;

-- 6. Vérifier que la table user_badge existe
CREATE TABLE IF NOT EXISTS user_badge (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL REFERENCES users(id),
    badge_id INTEGER NOT NULL REFERENCES badges(id),
    progression REAL DEFAULT 1.0 NOT NULL,
    awarded_at DATETIME
);

-- 7. Insérer quelques badges par défaut si la table est vide
INSERT OR IGNORE INTO badges (name, description, criteria, image_url, secret) VALUES 
('Premier Quiz', 'A réussi son premier quiz', '{"type": "quiz_completed", "count": 1}', '/badges/first-quiz.png', 0),
('Excellent Score', 'A obtenu un score parfait', '{"type": "perfect_score", "percentage": 100}', '/badges/perfect.png', 0),
('Participant Actif', 'A participé à plusieurs quiz', '{"type": "quiz_participation", "count": 5}', '/badges/active.png', 0);

-- 8. Vérifier que la table quiz_assignments existe
CREATE TABLE IF NOT EXISTS quiz_assignments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id),
    class_id INTEGER REFERENCES class_groups(id),
    student_id INTEGER REFERENCES users(id),
    assigned_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    due_date DATETIME
);

-- 9. Vérifier que la table questions existe
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    quiz_id INTEGER NOT NULL REFERENCES quizzes(id),
    question_text TEXT NOT NULL,
    question_type VARCHAR NOT NULL,
    points REAL DEFAULT 1.0,
    "order" INTEGER DEFAULT 0,
    options TEXT, -- JSON stocké comme texte
    correct_answer TEXT -- JSON stocké comme texte
);

-- 10. Vérifier que la table quiz_answers existe
CREATE TABLE IF NOT EXISTS quiz_answers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    result_id INTEGER NOT NULL REFERENCES quiz_results(id),
    question_id INTEGER NOT NULL REFERENCES questions(id),
    student_answer TEXT,
    is_correct BOOLEAN,
    points_earned REAL DEFAULT 0
);

-- Afficher le statut des tables
SELECT 'Tables vérifiées et corrigées' as status; 