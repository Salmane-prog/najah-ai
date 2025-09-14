-- =====================================================
-- SCRIPT D'INSERTION DE DONNÉES DE TEST
-- =====================================================

-- 1. Insérer des utilisateurs de test
INSERT INTO users (username, email, hashed_password, role, first_name, last_name, avatar) VALUES
('admin', 'admin@najah.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8HqHh6.', 'admin', 'Admin', 'System', 'A'),
('teacher1', 'marie.dubois@najah.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8HqHh6.', 'teacher', 'Marie', 'Dubois', 'MD'),
('teacher2', 'ahmed.benali@najah.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8HqHh6.', 'teacher', 'Ahmed', 'Benali', 'AB'),
('student1', 'salmane.hajouji@najah.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8HqHh6.', 'student', 'Salmane', 'EL Hajouji', 'SH'),
('student2', 'fatima.alami@najah.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8HqHh6.', 'student', 'Fatima', 'Alami', 'FA'),
('student3', 'omar.benjelloun@najah.ai', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj4J/8HqHh6.', 'student', 'Omar', 'Benjelloun', 'OB')
ON CONFLICT (username) DO NOTHING;

-- 2. Insérer des catégories
INSERT INTO categories (name, description, icon, color) VALUES
('Français', 'Cours et exercices de français', '📚', '#3B82F6'),
('Mathématiques', 'Cours et exercices de mathématiques', '🔢', '#10B981'),
('Histoire', 'Cours et exercices d''histoire', '🏛️', '#F59E0B'),
('Sciences', 'Cours et exercices de sciences', '🔬', '#EF4444'),
('Anglais', 'Cours et exercices d''anglais', '🇬🇧', '#8B5CF6')
ON CONFLICT DO NOTHING;

-- 3. Insérer des classes
INSERT INTO class_groups (name, description, teacher_id, subject, level, max_students) VALUES
('Français Avancé', 'Classe de français niveau avancé', 2, 'Français', 'Avancé', 25),
('Mathématiques Intermédiaire', 'Classe de mathématiques niveau intermédiaire', 3, 'Mathématiques', 'Intermédiaire', 30),
('Histoire Débutant', 'Classe d''histoire niveau débutant', 2, 'Histoire', 'Débutant', 20)
ON CONFLICT DO NOTHING;

-- 4. Inscrire des étudiants dans les classes
INSERT INTO class_students (class_id, student_id, status) VALUES
(1, 4, 'active'),
(1, 5, 'active'),
(2, 4, 'active'),
(2, 6, 'active'),
(3, 5, 'active'),
(3, 6, 'active')
ON CONFLICT DO NOTHING;

-- 5. Insérer des badges
INSERT INTO badges (name, description, icon, badge_type, xp_reward) VALUES
('Premier Quiz', 'Compléter votre premier quiz', '🎯', 'achievement', 50),
('Étudiant Assidu', 'Compléter 10 quiz', '📚', 'achievement', 200),
('Expert Français', 'Obtenir 90% en français', '🏆', 'achievement', 500),
('Niveau 5', 'Atteindre le niveau 5', '⭐', 'level', 100),
('Série de 7 jours', 'Se connecter 7 jours de suite', '🔥', 'streak', 300)
ON CONFLICT DO NOTHING;

-- 6. Insérer des niveaux utilisateurs
INSERT INTO user_levels (user_id, level, current_xp, total_xp, xp_to_next_level) VALUES
(4, 3, 250, 2250, 750),
(5, 2, 150, 1150, 850),
(6, 1, 50, 50, 950)
ON CONFLICT (user_id) DO UPDATE SET
    level = EXCLUDED.level,
    current_xp = EXCLUDED.current_xp,
    total_xp = EXCLUDED.total_xp,
    xp_to_next_level = EXCLUDED.xp_to_next_level;

-- 7. Insérer des quiz
INSERT INTO quizzes (title, description, subject, level, created_by, time_limit, total_points) VALUES
('Quiz Grammaire Française', 'Test de grammaire française de base', 'Français', 'Débutant', 2, 15, 20),
('Quiz Algèbre', 'Test d''algèbre niveau intermédiaire', 'Mathématiques', 'Intermédiaire', 3, 20, 25),
('Quiz Histoire de France', 'Test sur l''histoire de France', 'Histoire', 'Débutant', 2, 15, 20)
ON CONFLICT DO NOTHING;

-- 8. Insérer des questions pour le premier quiz
INSERT INTO questions (quiz_id, question_text, question_type, points, "order", options, correct_answer) VALUES
(1, 'Quelle est la fonction du mot "rapidement" dans la phrase "Il court rapidement" ?', 'mcq', 2, 1, 
 '["Sujet", "Verbe", "Complément d''objet", "Complément circonstanciel"]', '[3]'),
(1, 'Conjuguez le verbe "aller" à la première personne du pluriel au présent :', 'mcq', 2, 2,
 '["Je vais", "Tu vas", "Nous allons", "Ils vont"]', '[2]'),
(1, 'Quel est le pluriel de "cheval" ?', 'mcq', 2, 3,
 '["Chevals", "Chevaux", "Chevales", "Chevauxs"]', '[1]'),
(1, 'Identifiez la nature grammaticale du mot "beau" dans "un beau jardin" :', 'mcq', 2, 4,
 '["Nom", "Verbe", "Adjectif", "Adverbe"]', '[2]'),
(1, 'Quelle est la règle d''accord pour "des" dans "des enfants heureux" ?', 'mcq', 2, 5,
 '["Aucun accord", "Accord avec le nom", "Accord avec l''adjectif", "Accord avec le verbe"]', '[1]')
ON CONFLICT DO NOTHING;

-- 9. Insérer des résultats de quiz
INSERT INTO quiz_results (user_id, sujet, score, completed, quiz_id, student_id, max_score, percentage) VALUES
(4, 'Français', 16, 1, 1, 4, 20, 80.0),
(5, 'Français', 14, 1, 1, 5, 20, 70.0),
(4, 'Mathématiques', 20, 1, 2, 4, 25, 80.0),
(6, 'Mathématiques', 18, 1, 2, 6, 25, 72.0)
ON CONFLICT DO NOTHING;

-- 10. Insérer des contenus
INSERT INTO contents (title, description, content_type, subject, level, difficulty, estimated_time, created_by, category_id) VALUES
('Les Fondamentaux de la Grammaire', 'Cours complet sur les bases de la grammaire française', 'text', 'Français', 'Débutant', 3.0, 45, 2, 1),
('Algèbre Fondamentale', 'Introduction aux concepts d''algèbre', 'text', 'Mathématiques', 'Intermédiaire', 5.0, 60, 3, 2),
('La Révolution Française', 'Cours sur la Révolution française et ses conséquences', 'text', 'Histoire', 'Débutant', 4.0, 90, 2, 3)
ON CONFLICT DO NOTHING;

-- 11. Insérer des parcours d'apprentissage
INSERT INTO learning_paths (title, description, subject, level, difficulty, estimated_duration) VALUES
('Parcours Français Complet', 'Parcours complet pour maîtriser le français', 'Français', 'Débutant', 'Intermédiaire', 480),
('Parcours Mathématiques Avancé', 'Parcours pour les mathématiques avancées', 'Mathématiques', 'Intermédiaire', 'Avancé', 600),
('Parcours Histoire de France', 'Découverte de l''histoire de France', 'Histoire', 'Débutant', 'Intermédiaire', 360)
ON CONFLICT DO NOTHING;

-- 12. Insérer des messages de test
INSERT INTO threads (title, created_by, thread_type) VALUES
('Questions générales', 4, 'general'),
('Support technique', 4, 'support'),
('Discussion sur les cours', 2, 'discussion')
ON CONFLICT DO NOTHING;

INSERT INTO messages (user_id, content, thread_id) VALUES
(4, 'Bonjour ! J''ai une question sur le cours de grammaire.', 1),
(2, 'Bonjour ! Je peux vous aider avec votre question.', 1),
(4, 'Merci beaucoup !', 1),
(4, 'J''ai un problème technique avec la plateforme.', 2),
(1, 'Nous allons résoudre votre problème rapidement.', 2)
ON CONFLICT DO NOTHING;

-- 13. Insérer des badges utilisateurs
INSERT INTO user_badges (user_id, badge_id, progression, unlocked_at) VALUES
(4, 1, 1.0, CURRENT_TIMESTAMP),
(4, 4, 1.0, CURRENT_TIMESTAMP),
(5, 1, 1.0, CURRENT_TIMESTAMP),
(6, 1, 1.0, CURRENT_TIMESTAMP)
ON CONFLICT DO NOTHING;

-- 14. Insérer des défis
INSERT INTO challenges (title, description, challenge_type, xp_reward, badge_reward_id) VALUES
('Quiz Quotidien', 'Compléter un quiz chaque jour cette semaine', 'daily', 100, 1),
('Expert en Grammaire', 'Obtenir 100% sur un quiz de grammaire', 'achievement', 200, 3),
('Série d''Apprentissage', 'Se connecter 5 jours de suite', 'weekly', 150, 5)
ON CONFLICT DO NOTHING;

-- 15. Insérer des défis utilisateurs
INSERT INTO user_challenges (user_id, challenge_id, progress, is_completed) VALUES
(4, 1, 0.7, FALSE),
(4, 2, 0.8, FALSE),
(5, 1, 0.3, FALSE),
(6, 1, 0.5, FALSE)
ON CONFLICT DO NOTHING;

-- 16. Insérer des classements
INSERT INTO leaderboards (title, description, leaderboard_type, subject, is_active) VALUES
('Classement Global', 'Classement général de tous les étudiants', 'global', NULL, TRUE),
('Classement Français', 'Classement spécifique au français', 'subject', 'Français', TRUE),
('Classement Mathématiques', 'Classement spécifique aux mathématiques', 'subject', 'Mathématiques', TRUE)
ON CONFLICT DO NOTHING;

INSERT INTO leaderboard_entries (leaderboard_id, user_id, score, rank) VALUES
(1, 4, 2250, 1),
(1, 5, 1150, 2),
(1, 6, 50, 3),
(2, 4, 80, 1),
(2, 5, 70, 2),
(3, 4, 80, 1),
(3, 6, 72, 2)
ON CONFLICT DO NOTHING;

-- 17. Insérer des réalisations
INSERT INTO achievements (title, description, icon, achievement_type, xp_reward) VALUES
('Premier Pas', 'Compléter votre premier quiz', '🎯', 'quiz', 50),
('Étudiant Assidu', 'Compléter 10 quiz', '📚', 'quiz', 200),
('Expert Français', 'Obtenir 90% en français', '🏆', 'quiz', 500),
('Niveau 5', 'Atteindre le niveau 5', '⭐', 'level', 100),
('Série de 7 jours', 'Se connecter 7 jours de suite', '🔥', 'streak', 300)
ON CONFLICT DO NOTHING;

-- 18. Insérer des réalisations utilisateurs
INSERT INTO user_achievements (user_id, achievement_id) VALUES
(4, 1),
(4, 4),
(5, 1),
(6, 1)
ON CONFLICT DO NOTHING;

-- 19. Insérer des notes
INSERT INTO notes (user_id, title, content, content_id) VALUES
(4, 'Notes sur la grammaire', 'Les règles de conjugaison sont importantes à retenir.', 1),
(5, 'Notes sur l''algèbre', 'Les équations du premier degré sont la base.', 2),
(6, 'Notes sur l''histoire', 'La Révolution française a eu un impact majeur.', 3)
ON CONFLICT DO NOTHING;

-- 20. Insérer des évaluations
INSERT INTO assessments (student_id, assessment_type, title, description, status) VALUES
(4, 'initial', 'Évaluation Initiale - Français', 'Test de niveau en français', 'completed'),
(5, 'initial', 'Évaluation Initiale - Mathématiques', 'Test de niveau en mathématiques', 'in_progress'),
(6, 'initial', 'Évaluation Initiale - Histoire', 'Test de niveau en histoire', 'not_started')
ON CONFLICT DO NOTHING;

-- =====================================================
-- VÉRIFICATION DES DONNÉES INSÉRÉES
-- =====================================================

-- Vérifier le nombre d'utilisateurs
SELECT 'Utilisateurs' as table_name, COUNT(*) as count FROM users
UNION ALL
SELECT 'Catégories', COUNT(*) FROM categories
UNION ALL
SELECT 'Classes', COUNT(*) FROM class_groups
UNION ALL
SELECT 'Étudiants en classe', COUNT(*) FROM class_students
UNION ALL
SELECT 'Quiz', COUNT(*) FROM quizzes
UNION ALL
SELECT 'Questions', COUNT(*) FROM questions
UNION ALL
SELECT 'Résultats de quiz', COUNT(*) FROM quiz_results
UNION ALL
SELECT 'Contenus', COUNT(*) FROM contents
UNION ALL
SELECT 'Parcours', COUNT(*) FROM learning_paths
UNION ALL
SELECT 'Messages', COUNT(*) FROM messages
UNION ALL
SELECT 'Badges', COUNT(*) FROM badges
UNION ALL
SELECT 'Badges utilisateurs', COUNT(*) FROM user_badges
UNION ALL
SELECT 'Niveaux utilisateurs', COUNT(*) FROM user_levels
UNION ALL
SELECT 'Défis', COUNT(*) FROM challenges
UNION ALL
SELECT 'Défis utilisateurs', COUNT(*) FROM user_challenges
UNION ALL
SELECT 'Classements', COUNT(*) FROM leaderboards
UNION ALL
SELECT 'Entrées classements', COUNT(*) FROM leaderboard_entries
UNION ALL
SELECT 'Réalisations', COUNT(*) FROM achievements
UNION ALL
SELECT 'Réalisations utilisateurs', COUNT(*) FROM user_achievements
UNION ALL
SELECT 'Notes', COUNT(*) FROM notes
UNION ALL
SELECT 'Évaluations', COUNT(*) FROM assessments;

-- Afficher les utilisateurs avec leurs niveaux
SELECT 
    u.username,
    u.role,
    ul.level,
    ul.current_xp,
    ul.total_xp
FROM users u
LEFT JOIN user_levels ul ON u.id = ul.user_id
ORDER BY u.role, ul.total_xp DESC;

-- Afficher les résultats de quiz
SELECT 
    u.username,
    qr.sujet,
    qr.score,
    qr.max_score,
    qr.percentage
FROM quiz_results qr
JOIN users u ON qr.user_id = u.id
ORDER BY qr.percentage DESC;

-- =====================================================
-- MESSAGE DE SUCCÈS
-- =====================================================
SELECT '✅ DONNÉES DE TEST INSÉRÉES AVEC SUCCÈS !' as status;
SELECT 'Votre base de données est maintenant prête pour le développement.' as message; 