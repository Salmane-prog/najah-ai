#!/usr/bin/env node

/**
 * Script de test pour vérifier le debugging du dashboard
 */

console.log('🔍 Test de debugging du dashboard...\n');

console.log('📋 Instructions de test :');
console.log('   1. Redémarrer le serveur frontend : npm run dev');
console.log('   2. Aller sur /dashboard/student');
console.log('   3. Ouvrir la console du navigateur (F12)');
console.log('   4. Regarder les logs de debugging :');

console.log('\n🔍 Logs à vérifier dans la console :');
console.log('   - "🔍 useStudentDashboard - Données calculées:"');
console.log('   - "🔍 UnifiedStatsWidget - Données reçues:"');

console.log('\n📊 Données attendues :');
console.log('   - quizResultsCount: devrait être > 0');
console.log('   - calculatedStats.completedQuizzes: devrait être 10');
console.log('   - calculatedStats.averageScore: devrait être > 0');
console.log('   - stats.completedQuizzes: devrait être 10 (pas 0)');

console.log('\n🚨 Si les données sont toujours 0 :');
console.log('   1. Vérifier que le serveur backend fonctionne');
console.log('   2. Vérifier que l\'API retourne des données');
console.log('   3. Vérifier que ScoreCalculator fonctionne');
console.log('   4. Vérifier que les données arrivent au widget');

console.log('\n🎯 Résultat attendu :');
console.log('   - Console affiche les vraies valeurs calculées');
console.log('   - Interface affiche 10 Quiz Complétés');
console.log('   - Interface affiche le vrai Score Moyen');

console.log('\n✨ Debugging activé !');
console.log('   Vérifiez la console du navigateur pour voir les données !');


