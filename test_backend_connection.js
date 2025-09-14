#!/usr/bin/env node

/**
 * Script de test de connectivité au backend
 */

console.log('🔍 Test de connectivité au backend...\n');

// Test des différentes URLs possibles
const testUrls = [
  'http://localhost:8000',
  'http://127.0.0.1:8000',
  'http://0.0.0.0:8000'
];

console.log('📋 URLs à tester :');
testUrls.forEach(url => console.log(`   - ${url}`));

console.log('\n🚀 Instructions de test :');
console.log('   1. Ouvrir le navigateur');
console.log('   2. Tester chaque URL :');
console.log('      - http://localhost:8000/docs');
console.log('      - http://localhost:8000/health');
console.log('      - http://localhost:8000/');

console.log('\n🔧 Si le backend ne répond pas :');
console.log('   1. Vérifier que le terminal backend est actif');
console.log('   2. Vérifier qu\'il affiche "Application startup complete"');
console.log('   3. Vérifier qu\'il n\'y a pas d\'erreurs');

console.log('\n🎯 Résultats attendus :');
console.log('   - http://localhost:8000/docs → Page de documentation FastAPI');
console.log('   - http://localhost:8000/health → {"status": "ok"}');
console.log('   - http://localhost:8000/ → Page d\'accueil');

console.log('\n🚨 Si toujours "Failed to fetch" :');
console.log('   1. Problème de firewall Windows');
console.log('   2. Problème de port bloqué');
console.log('   3. Problème de configuration réseau');

console.log('\n✨ Solutions possibles :');
console.log('   1. Redémarrer le backend');
console.log('   2. Changer le port (8001 au lieu de 8000)');
console.log('   3. Vérifier les paramètres Windows Defender');

console.log('\n🎉 Test de connectivité activé !');
console.log('   Testez les URLs dans votre navigateur !');


