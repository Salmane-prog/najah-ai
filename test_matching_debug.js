#!/usr/bin/env node

/**
 * Script de test pour déboguer le problème de la page de matching
 * Vérifie que les items sont bien chargés et affichés
 */

const http = require('http');

console.log('🔍 [DEBUG MATCHING] Test de débogage de la page de matching...\n');

// Configuration
const FRONTEND_URL = 'http://localhost:3001';

// Tests à effectuer
const tests = [
  {
    name: 'Page de matching vocabulaire',
    url: `${FRONTEND_URL}/dashboard/student/remediation/matching/vocabulary`,
    expectedStatus: 200
  },
  {
    name: 'Page de matching grammaire',
    url: `${FRONTEND_URL}/dashboard/student/remediation/matching/grammar`,
    expectedStatus: 200
  },
  {
    name: 'Page de matching conjugaison',
    url: `${FRONTEND_URL}/dashboard/student/remediation/matching/conjugation`,
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
          
          // Vérifier la présence d'éléments de matching
          const hasMatchingTitle = content.includes('Exercice de Matching') || content.includes('matching');
          const hasInstructions = content.includes('Instructions') || content.includes('Associez');
          const hasLeftColumn = content.includes('Cliquez sur un élément à gauche');
          const hasRightColumn = content.includes('Puis cliquez sur sa correspondance à droite');
          const hasItems = content.includes('père') || content.includes('mère') || content.includes('maison') || content.includes('chat');
          
          console.log(`   🔍 Analyse du contenu:`);
          console.log(`      - Titre de matching: ${hasMatchingTitle ? '✅' : '❌'}`);
          console.log(`      - Instructions: ${hasInstructions ? '✅' : '❌'}`);
          console.log(`      - Colonne gauche: ${hasLeftColumn ? '✅' : '❌'}`);
          console.log(`      - Colonne droite: ${hasRightColumn ? '✅' : '❌'}`);
          console.log(`      - Items d'exercice: ${hasItems ? '✅' : '❌'}`);
          
          // Vérifier la présence de composants React
          const hasReactComponents = content.includes('__NEXT_DATA__') || content.includes('react');
          console.log(`      - Composants React: ${hasReactComponents ? '✅' : '❌'}`);
          
          // Rechercher des éléments spécifiques
          if (hasItems) {
            console.log(`   📝 Items trouvés dans le contenu:`);
            const itemMatches = content.match(/(père|mère|frère|sœur|maison|chat|livre|voiture)/g);
            if (itemMatches) {
              const uniqueItems = [...new Set(itemMatches)];
              console.log(`      - ${uniqueItems.join(', ')}`);
            }
          }
          
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
  console.log('🚀 [DEBUG MATCHING] Démarrage des tests de débogage...\n');
  
  const results = [];
  
  for (const test of tests) {
    const result = await testEndpoint(test);
    results.push(result);
    console.log(''); // Ligne vide pour la lisibilité
  }
  
  // Résumé des tests
  console.log('📊 [DEBUG MATCHING] Résumé des tests:');
  console.log('=====================================');
  
  const successfulTests = results.filter(r => r.success).length;
  const totalTests = results.length;
  
  results.forEach(result => {
    const status = result.success ? '✅' : '❌';
    console.log(`${status} ${result.test.name}: ${result.statusCode || 'Erreur'}`);
  });
  
  console.log(`\n🎯 [DEBUG MATCHING] Résultat: ${successfulTests}/${totalTests} tests réussis`);
  
  // Recommandations
  console.log('\n💡 [DEBUG MATCHING] Recommandations:');
  
  if (successfulTests === totalTests) {
    console.log('✅ Toutes les pages de matching sont accessibles');
    
    // Analyser la qualité du contenu
    const contentQuality = results.filter(r => r.success && r.data).map(r => {
      const content = r.data;
      const hasItems = content.includes('père') || content.includes('mère') || content.includes('maison') || content.includes('chat');
      const hasInstructions = content.includes('Instructions') || content.includes('Associez');
      
      return {
        test: r.test.name,
        hasItems,
        hasInstructions
      };
    });
    
    if (contentQuality.length > 0) {
      console.log('\n🔍 [DEBUG MATCHING] Analyse de la qualité du contenu:');
      contentQuality.forEach(quality => {
        console.log(`   📄 ${quality.test}:`);
        console.log(`      - Items d'exercice: ${quality.hasItems ? '✅' : '❌'}`);
        console.log(`      - Instructions: ${quality.hasInstructions ? '✅' : '❌'}`);
      });
      
      const pagesWithItems = contentQuality.filter(q => q.hasItems).length;
      const pagesWithInstructions = contentQuality.filter(q => q.hasInstructions).length;
      
      if (pagesWithItems === 0) {
        console.log('\n⚠️  [DEBUG MATCHING] PROBLÈME DÉTECTÉ:');
        console.log('   - Aucune page ne contient d\'items d\'exercice');
        console.log('   - Les exercices de matching ne se chargent pas correctement');
        console.log('   - Vérifiez la logique de chargement des exercices');
      } else if (pagesWithItems < totalTests) {
        console.log('\n⚠️  [DEBUG MATCHING] PROBLÈME PARTIEL:');
        console.log(`   - ${pagesWithItems}/${totalTests} pages contiennent des items`);
        console.log('   - Certains exercices de matching ne se chargent pas');
      } else {
        console.log('\n✅ [DEBUG MATCHING] Tous les exercices de matching fonctionnent correctement !');
      }
    }
    
  } else {
    console.log('❌ Certaines pages de matching sont inaccessibles');
    console.log('💡 Vérifiez que le serveur Next.js est démarré et que les routes sont correctes');
  }
}

// Démarrer les tests
runTests().catch(error => {
  console.error('💥 [DEBUG MATCHING] Erreur lors de l\'exécution des tests:', error);
  process.exit(1);
});






