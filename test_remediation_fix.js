#!/usr/bin/env node

/**
 * Script de test pour vérifier la page de remédiation
 * Teste les différents composants et fonctionnalités
 */

const http = require('http');

console.log('🧪 [TEST REMEDIATION] Début des tests de la page de remédiation...\n');

// Configuration
const FRONTEND_URL = 'http://localhost:3001';
const BACKEND_URL = 'http://localhost:8000';

// Tests à effectuer
const tests = [
  {
    name: 'Test de la page de remédiation (Frontend)',
    url: `${FRONTEND_URL}/dashboard/student/remediation`,
    expectedStatus: 200
  },
  {
    name: 'Test de l\'endpoint de remédiation (Backend)',
    url: `${BACKEND_URL}/api/v1/remediation/health`,
    expectedStatus: 200
  },
  {
    name: 'Test de l\'endpoint des exercices diversifiés (Backend)',
    url: `${BACKEND_URL}/api/v1/remediation/exercises/test-public`,
    expectedStatus: 200
  },
  {
    name: 'Test de l\'endpoint des statistiques (Backend)',
    url: `${BACKEND_URL}/api/v1/remediation/exercises/statistics`,
    expectedStatus: 401 // Doit retourner 401 car pas d'authentification
  }
];

// Fonction pour effectuer un test HTTP
function testEndpoint(test) {
  return new Promise((resolve) => {
    console.log(`🔍 [TEST] ${test.name}...`);
    
    const req = http.get(test.url, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        const success = res.statusCode === test.expectedStatus;
        const status = success ? '✅' : '❌';
        
        console.log(`${status} ${test.name}: ${res.statusCode} ${res.statusMessage}`);
        
        if (success) {
          console.log(`   📊 Réponse reçue: ${data.length} caractères`);
        } else {
          console.log(`   ⚠️  Attendu: ${test.expectedStatus}, Reçu: ${res.statusCode}`);
        }
        
        resolve({ test, success, statusCode: res.statusCode, data });
      });
    });
    
    req.on('error', (error) => {
      console.log(`❌ ${test.name}: Erreur de connexion - ${error.message}`);
      resolve({ test, success: false, error: error.message });
    });
    
    req.setTimeout(5000, () => {
      console.log(`⏰ ${test.name}: Timeout de la requête`);
      req.destroy();
      resolve({ test, success: false, error: 'Timeout' });
    });
  });
}

// Fonction principale de test
async function runTests() {
  console.log('🚀 [TEST REMEDIATION] Démarrage des tests...\n');
  
  const results = [];
  
  for (const test of tests) {
    const result = await testEndpoint(test);
    results.push(result);
    console.log(''); // Ligne vide pour la lisibilité
  }
  
  // Résumé des tests
  console.log('📊 [TEST REMEDIATION] Résumé des tests:');
  console.log('=====================================');
  
  const successfulTests = results.filter(r => r.success).length;
  const totalTests = results.length;
  
  results.forEach(result => {
    const status = result.success ? '✅' : '❌';
    console.log(`${status} ${result.test.name}: ${result.statusCode || 'Erreur'}`);
  });
  
  console.log(`\n🎯 [TEST REMEDIATION] Résultat: ${successfulTests}/${totalTests} tests réussis`);
  
  if (successfulTests === totalTests) {
    console.log('🎉 [TEST REMEDIATION] Tous les tests sont passés avec succès !');
  } else {
    console.log('⚠️  [TEST REMEDIATION] Certains tests ont échoué. Vérifiez la configuration.');
  }
  
  // Recommandations
  console.log('\n💡 [TEST REMEDIATION] Recommandations:');
  
  if (results[0].success) {
    console.log('✅ Frontend accessible - La page de remédiation devrait fonctionner');
  } else {
    console.log('❌ Frontend inaccessible - Vérifiez que le serveur Next.js est démarré sur le port 3001');
  }
  
  if (results[1].success) {
    console.log('✅ Backend accessible - L\'API de remédiation est opérationnelle');
  } else {
    console.log('❌ Backend inaccessible - Vérifiez que le serveur FastAPI est démarré sur le port 8000');
  }
  
  if (results[2].success) {
    console.log('✅ Endpoint des exercices accessible - Les exercices peuvent être récupérés');
  } else {
    console.log('❌ Endpoint des exercices inaccessible - Vérifiez la configuration de l\'API');
  }
  
  if (results[3].statusCode === 401) {
    console.log('✅ Authentification requise - L\'endpoint des statistiques est correctement protégé');
  } else {
    console.log('⚠️  Problème d\'authentification - Vérifiez la configuration de sécurité');
  }
}

// Démarrer les tests
runTests().catch(error => {
  console.error('💥 [TEST REMEDIATION] Erreur lors de l\'exécution des tests:', error);
  process.exit(1);
});









