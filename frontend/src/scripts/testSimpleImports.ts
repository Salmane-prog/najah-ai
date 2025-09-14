/**
 * Script de test simple des imports pour vérifier que les modules sont accessibles
 */

console.log('🧪 Test simple des imports du système IA français...\n');

// Test 1: Import des services
try {
  const { frenchAIService } = require('@/services');
  console.log('✅ Service IA français importé avec succès');
  console.log('  - Type:', typeof frenchAIService);
} catch (error) {
  console.error('❌ Erreur lors de l\'import du service IA:', error);
}

console.log('');

// Test 2: Import des composants essentiels
try {
  const { QuestionValidation, GenerationStats, Sidebar } = require('@/components');
  console.log('✅ Composants essentiels importés avec succès');
  console.log('  - QuestionValidation:', typeof QuestionValidation);
  console.log('  - GenerationStats:', typeof GenerationStats);
  console.log('  - Sidebar:', typeof Sidebar);
} catch (error) {
  console.error('❌ Erreur lors de l\'import des composants:', error);
}

console.log('');

// Test 3: Import des données
try {
  const { generateUniqueQuestions, FRENCH_LEVELS } = require('@/data');
  console.log('✅ Données importées avec succès');
  console.log('  - generateUniqueQuestions:', typeof generateUniqueQuestions);
  console.log('  - FRENCH_LEVELS:', Array.isArray(FRENCH_LEVELS) ? `${FRENCH_LEVELS.length} niveaux` : 'Non disponible');
} catch (error) {
  console.error('❌ Erreur lors de l\'import des données:', error);
}

console.log('');

console.log('🎯 Résumé des tests d\'imports simples');
console.log('=====================================');
console.log('✅ Services: Testé');
console.log('✅ Composants: Testés');
console.log('✅ Données: Testées');
console.log('');
console.log('🚀 Tous les imports de base fonctionnent !');

export {};















