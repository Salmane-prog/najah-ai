/**
 * Script de test de la génération de questions françaises
 */

import { generateUniqueQuestions } from '../data/frenchQuestionsBank';

console.log('🧪 Test de génération de questions françaises');
console.log('=============================================\n');

// Test 1: Génération de 20 questions pour le niveau Intermédiaire
console.log('📋 Test 1: Génération de 20 questions pour Intermédiaire (4-6)');
try {
  const questions20 = generateUniqueQuestions('Intermédiaire (4-6)', 20);
  console.log(`✅ Questions générées: ${questions20.length}`);
  
  if (questions20.length === 20) {
    console.log('🎯 SUCCÈS: Le bon nombre de questions a été généré');
  } else {
    console.log(`❌ ÉCHEC: ${questions20.length} questions au lieu de 20`);
  }
  
  // Vérifier l'unicité
  const uniqueQuestions = new Set(questions20.map(q => q.question));
  console.log(`🔍 Questions uniques: ${uniqueQuestions.size}/${questions20.length}`);
  
  if (uniqueQuestions.size === questions20.length) {
    console.log('✅ SUCCÈS: Toutes les questions sont uniques');
  } else {
    console.log('❌ ÉCHEC: Des doublons ont été détectés');
  }
  
} catch (error) {
  console.error('❌ Erreur lors du test 1:', error);
}

console.log('\n' + '='.repeat(50) + '\n');

// Test 2: Génération de 50 questions pour le niveau Avancé
console.log('📋 Test 2: Génération de 50 questions pour Avancé (7-9)');
try {
  const questions50 = generateUniqueQuestions('Avancé (7-9)', 50);
  console.log(`✅ Questions générées: ${questions50.length}`);
  
  if (questions50.length === 50) {
    console.log('🎯 SUCCÈS: Le bon nombre de questions a été généré');
  } else {
    console.log(`❌ ÉCHEC: ${questions50.length} questions au lieu de 50`);
  }
  
  // Vérifier l'unicité
  const uniqueQuestions = new Set(questions50.map(q => q.question));
  console.log(`🔍 Questions uniques: ${uniqueQuestions.size}/${questions50.length}`);
  
  if (uniqueQuestions.size === questions50.length) {
    console.log('✅ SUCCÈS: Toutes les questions sont uniques');
  } else {
    console.log('❌ ÉCHEC: Des doublons ont été détectés');
  }
  
} catch (error) {
  console.error('❌ Erreur lors du test 2:', error);
}

console.log('\n' + '='.repeat(50) + '\n');

// Test 3: Vérification des niveaux disponibles
console.log('📋 Test 3: Vérification des niveaux disponibles');
const levels = ['Débutant (1-3)', 'Intermédiaire (4-6)', 'Avancé (7-9)', 'Expert (10-12)'];

levels.forEach(level => {
  try {
    const questions = generateUniqueQuestions(level, 10);
    console.log(`✅ ${level}: ${questions.length} questions générées`);
  } catch (error) {
    console.error(`❌ ${level}: Erreur -`, error);
  }
});

console.log('\n' + '='.repeat(50) + '\n');

// Test 4: Performance et robustesse
console.log('📋 Test 4: Test de performance et robustesse');
const startTime = Date.now();

try {
  const questions100 = generateUniqueQuestions('Expert (10-12)', 100);
  const endTime = Date.now();
  const duration = endTime - startTime;
  
  console.log(`✅ 100 questions générées en ${duration}ms`);
  console.log(`📊 Taux de génération: ${(100 / (duration / 1000)).toFixed(2)} questions/seconde`);
  
  if (questions100.length === 100) {
    console.log('🎯 SUCCÈS: Génération de 100 questions réussie');
  } else {
    console.log(`❌ ÉCHEC: ${questions100.length} questions au lieu de 100`);
  }
  
} catch (error) {
  console.error('❌ Erreur lors du test de performance:', error);
}

console.log('\n' + '='.repeat(50) + '\n');
console.log('🏁 Tests terminés');
