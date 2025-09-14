-- =====================================================
-- SCRIPT DE TEST POUR VÉRIFIER LA BASE DE DONNÉES
-- =====================================================

-- 1. Vérifier que toutes les tables existent
SELECT 
    table_name,
    table_type
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE'
ORDER BY table_name;

-- 2. Compter le nombre total de tables
SELECT 
    COUNT(*) as total_tables
FROM information_schema.tables 
WHERE table_schema = 'public' 
AND table_type = 'BASE TABLE';

-- 3. Vérifier les contraintes de clés étrangères
SELECT 
    tc.table_name, 
    kcu.column_name, 
    ccu.table_name AS foreign_table_name,
    ccu.column_name AS foreign_column_name 
FROM 
    information_schema.table_constraints AS tc 
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
WHERE tc.constraint_type = 'FOREIGN KEY'
ORDER BY tc.table_name, kcu.column_name;

-- 4. Vérifier les index créés
SELECT 
    schemaname,
    tablename,
    indexname,
    indexdef
FROM pg_indexes 
WHERE schemaname = 'public'
ORDER BY tablename, indexname;

-- 5. Vérifier les triggers
SELECT 
    trigger_name,
    event_manipulation,
    event_object_table,
    action_statement
FROM information_schema.triggers
WHERE trigger_schema = 'public'
ORDER BY event_object_table, trigger_name;

-- 6. Vérifier les vues créées
SELECT 
    table_name,
    view_definition
FROM information_schema.views 
WHERE table_schema = 'public'
ORDER BY table_name;

-- 7. Vérifier les fonctions créées
SELECT 
    routine_name,
    routine_type,
    data_type
FROM information_schema.routines 
WHERE routine_schema = 'public'
ORDER BY routine_name;

-- 8. Test de connexion et permissions
SELECT current_database() as database_name;
SELECT current_user as current_user;
SELECT version();

-- 9. Vérifier l'espace disque utilisé
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) as size
FROM pg_tables 
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- 10. Test d'insertion dans une table (optionnel - pour vérifier les permissions)
-- INSERT INTO users (username, email, hashed_password, role) 
-- VALUES ('test_user', 'test@example.com', 'hashed_password', 'student')
-- ON CONFLICT DO NOTHING;

-- 11. Vérifier les contraintes CHECK
SELECT 
    tc.table_name,
    tc.constraint_name,
    cc.check_clause
FROM information_schema.table_constraints tc
JOIN information_schema.check_constraints cc 
    ON tc.constraint_name = cc.constraint_name
WHERE tc.constraint_type = 'CHECK'
AND tc.table_schema = 'public'
ORDER BY tc.table_name;

-- 12. Résumé des tables avec leurs colonnes principales
SELECT 
    t.table_name,
    COUNT(c.column_name) as column_count,
    STRING_AGG(c.column_name, ', ' ORDER BY c.ordinal_position) as columns
FROM information_schema.tables t
JOIN information_schema.columns c ON t.table_name = c.table_name
WHERE t.table_schema = 'public' 
AND t.table_type = 'BASE TABLE'
AND c.table_schema = 'public'
GROUP BY t.table_name
ORDER BY t.table_name;

-- =====================================================
-- RÉSULTATS ATTENDUS
-- =====================================================
/*
Vous devriez voir :

1. 28 tables créées :
   - users, categories, class_groups, class_students
   - quizzes, questions, quiz_results, quiz_answers, quiz_assignments
   - assessments, assessment_questions, assessment_results
   - contents, learning_paths, learning_path_contents, learning_history
   - threads, messages, notes
   - badges, user_badges, user_levels
   - challenges, user_challenges
   - leaderboards, leaderboard_entries
   - achievements, user_achievements

2. Des index sur les colonnes principales

3. Des triggers pour les mises à jour automatiques

4. Des vues pour les statistiques

5. Des fonctions pour les calculs

Si vous voyez ces résultats, votre base de données est correctement configurée !
*/ 