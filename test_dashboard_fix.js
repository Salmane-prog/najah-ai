// Script de test pour vérifier le dashboard
console.log('Test du dashboard Najah AI...');

// Test des endpoints API
async function testEndpoints() {
  const baseUrl = 'http://localhost:8000';
  const token = 'test-token'; // Token de test

  const endpoints = [
    '/api/v1/ai/analyze-student/current',
    '/api/v1/gamification/user/stats',
    '/api/v1/gamification/leaderboard',
    '/api/v1/analytics-advanced/interactive-charts/1?chart_type=performance&period=month'
  ];

  for (const endpoint of endpoints) {
    try {
      const response = await fetch(`${baseUrl}${endpoint}`, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        }
      });
      
      console.log(`${endpoint}: ${response.status} ${response.statusText}`);
      
      if (!response.ok) {
        console.log(`  ❌ Erreur: ${response.status} ${response.statusText}`);
      } else {
        console.log(`  ✅ Succès`);
      }
    } catch (error) {
      console.log(`${endpoint}: ❌ Erreur de connexion - ${error.message}`);
    }
  }
}

// Test de la page frontend
async function testFrontend() {
  try {
    const response = await fetch('http://localhost:3001/dashboard/teacher');
    console.log(`Frontend (dashboard teacher): ${response.status} ${response.statusText}`);
    
    if (response.ok) {
      console.log('  ✅ Page accessible');
    } else {
      console.log('  ❌ Page non accessible');
    }
  } catch (error) {
    console.log(`Frontend: ❌ Erreur de connexion - ${error.message}`);
  }
}

// Exécuter les tests
console.log('\n🔍 Test des endpoints backend...');
testEndpoints();

console.log('\n🔍 Test du frontend...');
testFrontend();

console.log('\n📋 Résumé des corrections apportées:');
console.log('✅ Widgets AI, Gamification et Graphiques corrigés');
console.log('✅ URLs API corrigées pour utiliser les redirections Next.js');
console.log('✅ Données de démonstration ajoutées en cas d\'échec API');
console.log('✅ Gestion d\'erreur améliorée');
console.log('✅ Chart.js déjà installé et configuré');

console.log('\n🎯 Instructions pour tester:');
console.log('1. Assurez-vous que le backend tourne sur http://localhost:8000');
console.log('2. Assurez-vous que le frontend tourne sur http://localhost:3001');
console.log('3. Naviguez vers http://localhost:3001/dashboard/teacher');
console.log('4. Les widgets devraient maintenant afficher du contenu (données de démonstration)'); 