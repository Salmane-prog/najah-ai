-- Script SQL pour remplir la base de données avec du contenu pédagogique réel

-- 1. Nettoyer les tables existantes
DELETE FROM assessment_questions;
DELETE FROM assessment_results;
DELETE FROM assessments;
DELETE FROM questions;
DELETE FROM quizzes;
DELETE FROM categories;

-- 2. Créer les catégories par matière et niveau
INSERT INTO categories (name, description) VALUES
-- Primaire
('Mathématiques Primaire', 'Arithmétique et géométrie de base'),
('Français Primaire', 'Lecture, écriture et grammaire'),
('Anglais Primaire', 'Vocabulaire et expressions de base'),

-- Collège
('Mathématiques Collège', 'Algèbre et géométrie'),
('Français Collège', 'Grammaire et littérature'),
('Anglais Collège', 'Grammaire et communication'),
('Histoire Collège', 'Histoire de France et du monde'),
('Géographie Collège', 'Géographie physique et humaine'),
('Sciences Collège', 'Physique, chimie et biologie'),

-- Lycée
('Mathématiques Lycée', 'Analyse et géométrie avancée'),
('Français Lycée', 'Littérature et analyse de textes'),
('Anglais Lycée', 'Littérature anglaise et civilisation'),
('Histoire Lycée', 'Histoire moderne et contemporaine'),
('Géographie Lycée', 'Géographie économique et politique'),
('Physique Lycée', 'Mécanique, électricité et optique'),
('Chimie Lycée', 'Chimie générale et organique'),
('Biologie Lycée', 'Biologie cellulaire et génétique');

-- 3. Créer les quizzes par matière et niveau
INSERT INTO quizzes (title, description, subject, level, is_active) VALUES
-- Mathématiques Primaire
('Addition et Soustraction', 'Opérations de base', 'mathématiques', 'primaire', 1),
('Multiplication et Division', 'Tables de multiplication', 'mathématiques', 'primaire', 1),
('Géométrie de Base', 'Formes et mesures', 'mathématiques', 'primaire', 1),

-- Français Primaire
('Lecture et Compréhension', 'Compréhension de textes simples', 'français', 'primaire', 1),
('Grammaire de Base', 'Conjugaison et accords', 'français', 'primaire', 1),
('Vocabulaire', 'Enrichissement du vocabulaire', 'français', 'primaire', 1),

-- Anglais Primaire
('Vocabulaire de Base', 'Mots du quotidien', 'anglais', 'primaire', 1),
('Expressions Simples', 'Phrases courantes', 'anglais', 'primaire', 1),

-- Mathématiques Collège
('Algèbre de Base', 'Équations du premier degré', 'mathématiques', 'collège', 1),
('Géométrie', 'Théorèmes et calculs', 'mathématiques', 'collège', 1),
('Statistiques', 'Moyennes et graphiques', 'mathématiques', 'collège', 1),

-- Français Collège
('Grammaire Avancée', 'Analyse grammaticale', 'français', 'collège', 1),
('Littérature', 'Analyse de textes', 'français', 'collège', 1),

-- Sciences Collège
('Physique de Base', 'Mécanique et énergie', 'sciences', 'collège', 1),
('Chimie de Base', 'Atomes et molécules', 'sciences', 'collège', 1),
('Biologie', 'Le vivant et son évolution', 'sciences', 'collège', 1);

-- 4. Créer les questions par quiz

-- Mathématiques Primaire - Addition et Soustraction (Quiz ID: 1)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(1, 'Combien font 5 + 3 ?', '["7", "8", "9", "10"]', '8', 1, 'débutant'),
(1, 'Combien font 12 - 4 ?', '["6", "7", "8", "9"]', '8', 1, 'débutant'),
(1, 'Quel est le résultat de 15 + 7 ?', '["20", "21", "22", "23"]', '22', 2, 'intermédiaire'),
(1, 'Combien font 25 - 8 ?', '["15", "16", "17", "18"]', '17', 2, 'intermédiaire'),
(1, 'Quel est le résultat de 100 + 50 ?', '["140", "150", "160", "170"]', '150', 3, 'avancé');

-- Mathématiques Primaire - Multiplication et Division (Quiz ID: 2)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(2, 'Combien font 6 × 7 ?', '["40", "42", "44", "46"]', '42', 2, 'intermédiaire'),
(2, 'Combien font 8 × 9 ?', '["70", "72", "74", "76"]', '72', 2, 'intermédiaire'),
(2, 'Quel est le résultat de 56 ÷ 8 ?', '["6", "7", "8", "9"]', '7', 2, 'intermédiaire'),
(2, 'Combien font 4 × 12 ?', '["44", "46", "48", "50"]', '48', 3, 'avancé'),
(2, 'Quel est le résultat de 81 ÷ 9 ?', '["7", "8", "9", "10"]', '9', 3, 'avancé');

-- Français Primaire - Lecture et Compréhension (Quiz ID: 4)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(4, 'Dans la phrase "Le chat dort sur le canapé", quel est le sujet ?', '["Le chat", "dort", "sur", "le canapé"]', 'Le chat', 1, 'débutant'),
(4, 'Quel est le verbe dans la phrase "Les enfants jouent dans le jardin" ?', '["Les enfants", "jouent", "dans", "le jardin"]', 'jouent', 1, 'débutant'),
(4, 'Complétez : "Le petit garçon ___ dans la rue."', '["marcher", "marche", "marché", "marchait"]', 'marche', 2, 'intermédiaire'),
(4, 'Dans la phrase "La fleur rouge sent bon", quel est l''adjectif ?', '["La", "fleur", "rouge", "sent"]', 'rouge', 2, 'intermédiaire'),
(4, 'Quel est le complément dans "Le chien mange sa nourriture" ?', '["Le chien", "mange", "sa nourriture", "le"]', 'sa nourriture', 3, 'avancé');

-- Français Primaire - Grammaire de Base (Quiz ID: 5)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(5, 'Conjuguez le verbe "être" à la 1ère personne du singulier au présent :', '["Je suis", "Je es", "Je être", "Je suis"]', 'Je suis', 1, 'débutant'),
(5, 'Quel est le pluriel de "cheval" ?', '["chevals", "chevaux", "chevales", "cheval"]', 'chevaux', 2, 'intermédiaire'),
(5, 'Conjuguez "aller" à la 3ème personne du pluriel au présent :', '["ils vont", "ils allons", "ils allez", "ils vont"]', 'ils vont', 2, 'intermédiaire'),
(5, 'Quel est le féminin de "beau" ?', '["beau", "belle", "beaux", "belles"]', 'belle', 1, 'débutant'),
(5, 'Conjuguez "faire" à la 2ème personne du singulier au présent :', '["tu fais", "tu fait", "tu faire", "tu fais"]', 'tu fais', 3, 'avancé');

-- Anglais Primaire - Vocabulaire de Base (Quiz ID: 7)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(7, 'Comment dit-on "bonjour" en anglais ?', '["Goodbye", "Hello", "Thank you", "Please"]', 'Hello', 1, 'débutant'),
(7, 'Quel est le mot anglais pour "chat" ?', '["Dog", "Cat", "Bird", "Fish"]', 'Cat', 1, 'débutant'),
(7, 'Comment dit-on "merci" en anglais ?', '["Please", "Thank you", "Sorry", "Excuse me"]', 'Thank you', 1, 'débutant'),
(7, 'Quel est le mot anglais pour "maison" ?', '["House", "Home", "Building", "Room"]', 'House', 2, 'intermédiaire'),
(7, 'Comment dit-on "au revoir" en anglais ?', '["Hello", "Goodbye", "Thank you", "Please"]', 'Goodbye', 2, 'intermédiaire');

-- Mathématiques Collège - Algèbre de Base (Quiz ID: 9)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(9, 'Résolvez l''équation : x + 5 = 12', '["x = 5", "x = 7", "x = 12", "x = 17"]', 'x = 7', 2, 'intermédiaire'),
(9, 'Quelle est la valeur de x dans l''équation 2x = 10 ?', '["x = 3", "x = 5", "x = 8", "x = 10"]', 'x = 5', 2, 'intermédiaire'),
(9, 'Résolvez : 3x - 6 = 9', '["x = 3", "x = 5", "x = 7", "x = 9"]', 'x = 5', 3, 'avancé'),
(9, 'Quelle est la valeur de x dans l''équation 4x + 8 = 20 ?', '["x = 2", "x = 3", "x = 4", "x = 5"]', 'x = 3', 3, 'avancé'),
(9, 'Résolvez : 2x + 3 = 11', '["x = 3", "x = 4", "x = 5", "x = 6"]', 'x = 4', 2, 'intermédiaire');

-- Sciences Collège - Physique de Base (Quiz ID: 13)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(13, 'Quelle est l''unité de mesure de la force ?', '["Le mètre", "Le newton", "Le joule", "Le watt"]', 'Le newton', 2, 'intermédiaire'),
(13, 'Qu''est-ce que l''énergie cinétique ?', '["L''énergie de mouvement", "L''énergie de position", "L''énergie thermique", "L''énergie électrique"]', 'L''énergie de mouvement', 2, 'intermédiaire'),
(13, 'Quelle est la formule de l''énergie cinétique ?', '["E = mgh", "E = ½mv²", "E = mc²", "E = Fd"]', 'E = ½mv²', 3, 'avancé'),
(13, 'Quelle est l''unité de mesure de la vitesse ?', '["Le mètre", "Le mètre par seconde", "Le newton", "Le joule"]', 'Le mètre par seconde', 1, 'débutant'),
(13, 'Qu''est-ce que la gravité ?', '["Une force d''attraction", "Une force de répulsion", "Une énergie", "Une vitesse"]', 'Une force d''attraction', 2, 'intermédiaire');

-- Sciences Collège - Chimie de Base (Quiz ID: 14)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(14, 'Quel est le symbole chimique de l''hydrogène ?', '["H", "He", "O", "N"]', 'H', 1, 'débutant'),
(14, 'Quel est le symbole chimique de l''oxygène ?', '["H", "He", "O", "N"]', 'O', 1, 'débutant'),
(14, 'Quelle est la formule chimique de l''eau ?', '["H2O", "CO2", "O2", "N2"]', 'H2O', 2, 'intermédiaire'),
(14, 'Quel est le symbole chimique du carbone ?', '["C", "Ca", "Co", "Cu"]', 'C', 1, 'débutant'),
(14, 'Quelle est la formule chimique du dioxyde de carbone ?', '["H2O", "CO2", "O2", "N2"]', 'CO2', 2, 'intermédiaire');

-- Français Collège - Grammaire Avancée (Quiz ID: 11)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(11, 'Quel est le mode du verbe dans "Si j''avais su, je serais venu" ?', '["Indicatif", "Subjonctif", "Conditionnel", "Impératif"]', 'Conditionnel', 3, 'avancé'),
(11, 'Quel est le temps du verbe "avait mangé" ?', '["Présent", "Imparfait", "Plus-que-parfait", "Passé simple"]', 'Plus-que-parfait', 3, 'avancé'),
(11, 'Dans "Le livre que j''ai lu", "que" est :', '["Un pronom relatif", "Une conjonction", "Un adverbe", "Un déterminant"]', 'Un pronom relatif', 2, 'intermédiaire'),
(11, 'Quel est le genre de "amour" ?', '["Masculin", "Féminin", "Les deux", "Neutre"]', 'Masculin', 2, 'intermédiaire'),
(11, 'Quel est le pluriel de "travail" ?', '["travails", "travaux", "travailes", "travail"]', 'travaux', 2, 'intermédiaire');

-- Anglais Collège - Grammaire et Communication (Quiz ID: 8)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(8, 'Quel est le passé simple de "to go" ?', '["goed", "went", "gone", "going"]', 'went', 2, 'intermédiaire'),
(8, 'Comment dit-on "je vais" en anglais ?', '["I go", "I am going", "I will go", "I went"]', 'I am going', 2, 'intermédiaire'),
(8, 'Quel est le comparatif de "good" ?', '["gooder", "more good", "better", "best"]', 'better', 2, 'intermédiaire'),
(8, 'Comment dit-on "il y a" en anglais ?', '["there is", "there are", "there have", "there has"]', 'there is', 2, 'intermédiaire'),
(8, 'Quel est le superlatif de "bad" ?', '["bader", "more bad", "worse", "worst"]', 'worst', 3, 'avancé');

-- Mathématiques Collège - Géométrie (Quiz ID: 10)
INSERT INTO questions (quiz_id, question_text, options, correct_answer, points, difficulty) VALUES
(10, 'Quelle est la formule de l''aire d''un cercle ?', '["A = πr", "A = πr²", "A = 2πr", "A = 4πr²"]', 'A = πr²', 2, 'intermédiaire'),
(10, 'Quelle est la formule du périmètre d''un rectangle ?', '["P = l + L", "P = 2(l + L)", "P = l × L", "P = 2l + 2L"]', 'P = 2(l + L)', 2, 'intermédiaire'),
(10, 'Quel est le théorème de Pythagore ?', '["a² + b² = c²", "a + b = c", "a² = b² + c²", "a = b + c"]', 'a² + b² = c²', 3, 'avancé'),
(10, 'Quelle est la formule de l''aire d''un triangle ?', '["A = b × h", "A = ½(b × h)", "A = b + h", "A = 2(b + h)"]', 'A = ½(b × h)', 2, 'intermédiaire'),
(10, 'Quel est le volume d''un cube de côté a ?', '["V = a²", "V = a³", "V = 6a²", "V = 12a"]', 'V = a³', 3, 'avancé');

-- Affichage des résultats
SELECT 'Catégories créées' as type, COUNT(*) as count FROM categories
UNION ALL
SELECT 'Quizzes créés' as type, COUNT(*) as count FROM quizzes
UNION ALL
SELECT 'Questions créées' as type, COUNT(*) as count FROM questions; 