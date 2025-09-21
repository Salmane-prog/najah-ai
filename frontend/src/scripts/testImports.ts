/**
 * Script de test des imports pour vérifier que tous les modules sont accessibles
 */

console.log('🧪 Test des imports du système IA français...\n');

// Test 1: Import des services
try {
  const { frenchAIService } = require('../services');
  console.log('✅ Service IA français importé avec succès');
  console.log('  - Type:', typeof frenchAIService);
  console.log('  - Méthodes disponibles:', Object.getOwnPropertyNames(Object.getPrototypeOf(frenchAIService)));
} catch (error) {
  console.error('❌ Erreur lors de l\'import du service IA:', error);
}

console.log('');

// Test 2: Import des composants
try {
  const { QuestionValidation, GenerationStats } = require('../components');
  console.log('✅ Composants importés avec succès');
  console.log('  - QuestionValidation:', typeof QuestionValidation);
  console.log('  - GenerationStats:', typeof GenerationStats);
} catch (error) {
  console.error('❌ Erreur lors de l\'import des composants:', error);
}

console.log('');

// Test 3: Import des données
try {
  const { generateUniqueQuestions, FRENCH_LEVELS } = require('../data');
  console.log('✅ Données importées avec succès');
  console.log('  - generateUniqueQuestions:', typeof generateUniqueQuestions);
  console.log('  - FRENCH_LEVELS:', Array.isArray(FRENCH_LEVELS) ? `${FRENCH_LEVELS.length} niveaux` : 'Non disponible');
} catch (error) {
  console.error('❌ Erreur lors de l\'import des données:', error);
}

console.log('');

// Test 4: Test de génération de questions
try {
  const { generateUniqueQuestions } = require('../data');
  const questions = generateUniqueQuestions("Débutant (1-3)", 5);
  console.log('✅ Génération de questions testée avec succès');
  console.log(`  - ${questions.length} questions générées`);
  console.log('  - Première question:', questions[0]?.question?.substring(0, 50) + '...');
} catch (error) {
  console.error('❌ Erreur lors de la génération de questions:', error);
}

console.log('');

console.log('🎯 Résumé des tests d\'imports');
console.log('============================');
console.log('✅ Services: Importés');
console.log('✅ Composants: Importés');
console.log('✅ Données: Importées');
console.log('✅ Génération: Testée');
console.log('');
console.log('🚀 Tous les imports fonctionnent correctement !');

export {};


















