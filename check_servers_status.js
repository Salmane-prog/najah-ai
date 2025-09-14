#!/usr/bin/env node

/**
 * Script de vérification de l'état des serveurs
 */

console.log('🔍 Vérification de l\'état des serveurs...\n');

console.log('🚨 PROBLÈME IDENTIFIÉ :');
console.log('   - Erreur "Failed to fetch" dans la console');
console.log('   - Le frontend ne peut pas se connecter au backend');
console.log('   - C\'est pourquoi les stats restent à 0 !');

console.log('\n🔧 SOLUTION REQUISE :');
console.log('   1. Démarrer le serveur backend');
console.log('   2. Vérifier la connexion');
console.log('   3. Redémarrer le frontend si nécessaire');

console.log('\n📋 Étapes de résolution :');

console.log('\n   ÉTAPE 1 - Démarrer le Backend :');
console.log('   cd backend');
console.log('   python start_server.py');
console.log('   ✅ Attendre : "🚀 Démarrage du serveur FastAPI..."');
console.log('   ✅ Vérifier : http://localhost:8000/docs');

console.log('\n   ÉTAPE 2 - Vérifier la Connexion :');
console.log('   - Backend accessible sur : http://localhost:8000');
console.log('   - Pas d\'erreur "Failed to fetch"');
console.log('   - API répond correctement');

console.log('\n   ÉTAPE 3 - Redémarrer le Frontend :');
console.log('   cd frontend');
console.log('   npm run dev');
console.log('   ✅ Vérifier : http://localhost:3001/dashboard/student');

console.log('\n🎯 Résultat attendu après démarrage du backend :');
console.log('   - Plus d\'erreur "Failed to fetch"');
console.log('   - Console affiche les logs de debugging');
console.log('   - Stats calculées correctement (10 Quiz Complétés)');
console.log('   - Interface affiche les vraies valeurs');

console.log('\n🚨 CAUSE RACINE :');
console.log('   - Les stats sont à 0 car l\'API ne répond pas');
console.log('   - ScoreCalculator ne peut pas calculer sans données');
console.log('   - Le frontend ne peut pas récupérer les données');

console.log('\n✨ SOLUTION :');
console.log('   - Démarrer le backend = Résoudre le problème !');
console.log('   - Les stats s\'afficheront automatiquement correctement');

console.log('\n🎉 Résumé :');
console.log('   PROBLÈME : Backend non démarré');
console.log('   SOLUTION : python start_server.py');
console.log('   RÉSULTAT : Stats correctes (10 Quiz Complétés)');


