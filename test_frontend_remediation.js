#!/usr/bin/env node

/**
 * Script de test pour vérifier le fonctionnement du frontend de remédiation
 * Teste la page et les composants
 */

const http = require('http');

console.log('🧪 [TEST FRONTEND REMEDIATION] Test du frontend de remédiation...\n');

// Configuration
const FRONTEND_URL = 'http://localhost:3001';

// Tests à effectuer
const tests = [
  {
    name: 'Page principale de remédiation',
    url: `${FRONTEND_URL}/dashboard/student/remediation`,
    expectedStatus: 200
  },
  {
    name: 'Page de quiz de remédiation',
    url: `${FRONTEND_URL}/dashboard/student/remediation/quiz/grammar`,
    expectedStatus: 200
  },
  {
    name: 'Page de matching de remédiation',
    url: `${FRONTEND_URL}/dashboard/student/remediation/matching/vocabulary`,
    expectedStatus: 200
  },
  {
    name: 'Page de lecture de remédiation',
    url: `${FRONTEND_URL}/dashboard/student/remediation/reading/comprehension`,
    expectedStatus: 200
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
          
          // Analyser le contenu pour vérifier la présence d'éléments clés
          const content = data.toString();
          
          // Vérifier la présence d'éléments de remédiation
          const hasRemediationTitle = content.includes('Plan de Remédiation') || content.includes('Remédiation');
          const hasExercises = content.includes('exercice') || content.includes('quiz') || content.includes('Exercice');
          const hasProgress = content.includes('progrès') || content.includes('Progrès') || content.includes('progress');
          
          console.log(`   🔍 Analyse du contenu:`);
          console.log(`      - Titre de remédiation: ${hasRemediationTitle ? '✅' : '❌'}`);
          console.log(`      - Exercices: ${hasExercises ? '✅' : '❌'}`);
          console.log(`      - Progression: ${hasProgress ? '✅' : '❌'}`);
          
          // Vérifier la présence de composants React
          const hasReactComponents = content.includes('__NEXT_DATA__') || content.includes('react');
          console.log(`      - Composants React: ${hasReactComponents ? '✅' : '❌'}`);
          
        } else {
          console.log(`   ⚠️  Attendu: ${test.expectedStatus}, Reçu: ${res.statusCode}`);
        }
        
        resolve({ test, success, statusCode: res.statusCode, data: data.toString() });
      });
    });
    
    req.on('error', (error) => {
      console.log(`❌ ${test.name}: Erreur de connexion - ${error.message}`);
      resolve({ test, success: false, error: error.message });
    });
    
    req.setTimeout(10000, () => {
      console.log(`⏰ ${test.name}: Timeout de la requête`);
      req.destroy();
      resolve({ test, success: false, error: 'Timeout' });
    });
  });
}

// Fonction principale de test
async function runTests() {
  console.log('🚀 [TEST FRONTEND REMEDIATION] Démarrage des tests...\n');
  
  const results = [];
  
  for (const test of tests) {
    const result = await testEndpoint(test);
    results.push(result);
    console.log(''); // Ligne vide pour la lisibilité
  }
  
  // Résumé des tests
  console.log('📊 [TEST FRONTEND REMEDIATION] Résumé des tests:');
  console.log('==============================================');
  
  const successfulTests = results.filter(r => r.success).length;
  const totalTests = results.length;
  
  results.forEach(result => {
    const status = result.success ? '✅' : '❌';
    console.log(`${status} ${result.test.name}: ${result.statusCode || 'Erreur'}`);
  });
  
  console.log(`\n🎯 [TEST FRONTEND REMEDIATION] Résultat: ${successfulTests}/${totalTests} tests réussis`);
  
  if (successfulTests === totalTests) {
    console.log('🎉 [TEST FRONTEND REMEDIATION] Tous les tests sont passés avec succès !');
  } else {
    console.log('⚠️  [TEST FRONTEND REMEDIATION] Certains tests ont échoué. Vérifiez la configuration.');
  }
  
  // Recommandations
  console.log('\n💡 [TEST FRONTEND REMEDIATION] Recommandations:');
  
  if (results[0].success) {
    console.log('✅ Page principale accessible - La remédiation de base fonctionne');
  } else {
    console.log('❌ Page principale inaccessible - Vérifiez que le serveur Next.js est démarré sur le port 3001');
  }
  
  // Analyser les pages spécifiques
  const specificPages = results.slice(1);
  const workingSpecificPages = specificPages.filter(r => r.success).length;
  
  if (workingSpecificPages === specificPages.length) {
    console.log('✅ Toutes les pages spécialisées fonctionnent - Remédiation complète opérationnelle');
  } else if (workingSpecificPages > 0) {
    console.log(`⚠️  ${workingSpecificPages}/${specificPages.length} pages spécialisées fonctionnent - Remédiation partiellement opérationnelle`);
  } else {
    console.log('❌ Aucune page spécialisée ne fonctionne - Vérifiez les routes et composants');
  }
  
  // Vérifier la qualité du contenu
  const contentQuality = results.filter(r => r.success && r.data).map(r => {
    const content = r.data;
    const hasRemediationContent = content.includes('remédiation') || content.includes('Remédiation');
    const hasExercises = content.includes('exercice') || content.includes('quiz');
    const hasProgress = content.includes('progrès') || content.includes('progress');
    
    return {
      test: r.test.name,
      hasRemediationContent,
      hasExercises,
      hasProgress
    };
  });
  
  if (contentQuality.length > 0) {
    console.log('\n🔍 [TEST FRONTEND REMEDIATION] Analyse de la qualité du contenu:');
    contentQuality.forEach(quality => {
      console.log(`   📄 ${quality.test}:`);
      console.log(`      - Contenu de remédiation: ${quality.hasRemediationContent ? '✅' : '❌'}`);
      console.log(`      - Exercices: ${quality.hasExercises ? '✅' : '❌'}`);
      console.log(`      - Progression: ${quality.hasProgress ? '✅' : '❌'}`);
    });
  }
}

// Démarrer les tests
runTests().catch(error => {
  console.error('💥 [TEST FRONTEND REMEDIATION] Erreur lors de l\'exécution des tests:', error);
  process.exit(1);
});






