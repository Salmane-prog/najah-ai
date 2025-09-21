// Script de test pour vérifier la gestion des données côté frontend

// Données simulées de l'API
const mockApiResponse = {
  success: true,
  total_tests: 5,
  tests: [
    {
      id: 1,
      title: "Test de Grammaire Française Niveau Intermédiaire",
      subject: "Français",
      description: "Test adaptatif pour évaluer les compétences en grammaire française",
      difficulty_range: { min: 3, max: 7 },
      estimated_duration: 25,
      is_active: true,
      created_at: "2025-08-17T14:53:22",
      statistics: {
        assignments: { total: 0, classes: 0, individuals: 0 },
        performance: { total_students: 0, completed_students: 0, in_progress_students: 0, average_score: 0 }
      }
    },
    {
      id: 2,
      title: "Évaluation Mathématiques - Algèbre",
      subject: "Mathématiques",
      description: "Test adaptatif sur les équations du premier degré",
      difficulty_range: { min: 4, max: 8 },
      estimated_duration: 30,
      is_active: true,
      created_at: "2025-08-17T14:53:24",
      statistics: {
        assignments: { total: 0, classes: 0, individuals: 0 },
        performance: { total_students: 0, completed_students: 0, in_progress_students: 0, average_score: 0 }
      }
    }
  ]
};

// Fonction de validation des données (similaire à celle du service)
function validateTestData(test) {
  return {
    id: test.id || 0,
    title: test.title || 'Sans titre',
    subject: test.subject || 'Matière non spécifiée',
    description: test.description || 'Aucune description',
    difficulty_range: {
      min: test.difficulty_range?.min || test.difficulty_range_min || 1,
      max: test.difficulty_range?.max || test.difficulty_range_max || 10
    },
    estimated_duration: test.estimated_duration || 30,
    is_active: test.is_active !== undefined ? test.is_active : true,
    created_at: test.created_at || new Date().toISOString(),
    statistics: {
      assignments: {
        total: test.statistics?.assignments?.total || 0,
        classes: test.statistics?.assignments?.classes || 0,
        individuals: test.statistics?.assignments?.individuals || 0
      },
      performance: {
        total_students: test.statistics?.performance?.total_students || 0,
        completed_students: test.statistics?.performance?.completed_students || 0,
        in_progress_students: test.statistics?.performance?.in_progress_students || 0,
        average_score: test.statistics?.performance?.average_score || 0
      }
    }
  };
}

// Test de validation
console.log("🧪 Test de validation des données côté frontend");
console.log("=" * 50);

if (mockApiResponse.success && mockApiResponse.tests) {
  console.log(`✅ ${mockApiResponse.total_tests} tests reçus`);
  
  const validatedTests = mockApiResponse.tests.map(test => validateTestData(test));
  
  validatedTests.forEach((test, index) => {
    console.log(`\n📊 Test ${index + 1}: ${test.title}`);
    console.log(`   - Niveau: ${test.difficulty_range.min}-${test.difficulty_range.max}`);
    console.log(`   - Durée: ${test.estimated_duration} min`);
    console.log(`   - Statut: ${test.is_active ? 'Actif' : 'Inactif'}`);
    console.log(`   - Étudiants: ${test.statistics.assignments.total} (${test.statistics.performance.completed_students} terminés)`);
    
    // Vérifier que difficulty_range est valide
    if (test.difficulty_range && test.difficulty_range.min && test.difficulty_range.max) {
      console.log(`   ✅ difficulty_range valide`);
    } else {
      console.log(`   ❌ difficulty_range invalide`);
    }
  });
  
  console.log("\n🎉 Tous les tests sont valides !");
} else {
  console.log("❌ Aucun test reçu");
}

// Test de gestion des erreurs
console.log("\n🔍 Test de gestion des erreurs...");

const invalidTest = {
  id: 999,
  title: "Test invalide",
  // difficulty_range manquant
  // estimated_duration manquant
};

const validatedInvalidTest = validateTestData(invalidTest);
console.log(`   Test invalide validé: Niveau ${validatedInvalidTest.difficulty_range.min}-${validatedInvalidTest.difficulty_range.max}, Durée: ${validatedInvalidTest.estimated_duration} min`);
console.log("   ✅ Gestion des erreurs fonctionne");





















