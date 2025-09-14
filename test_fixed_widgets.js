console.log('🧪 TEST DES WIDGETS CORRIGÉS');

// Fonction pour tester une API
async function testAPI(url, description) {
  console.log(`\n🔍 Test: ${description}`);
  console.log(`URL: ${url}`);
  
  const token = localStorage.getItem('najah_token');
  if (!token) {
    console.log('❌ Pas de token');
    return false;
  }
  
  try {
    const response = await fetch(url, {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log(`Status: ${response.status}`);
    console.log(`OK: ${response.ok}`);
    
    if (response.ok) {
      const data = await response.json();
      console.log(`✅ Succès: ${typeof data === 'object' ? Object.keys(data).length : data.length} éléments`);
      return true;
    } else {
      const error = await response.text();
      console.log(`❌ Erreur: ${error}`);
      return false;
    }
  } catch (error) {
    console.log(`❌ Erreur réseau: ${error}`);
    return false;
  }
}

// Fonction pour tester tous les endpoints
async function testAllEndpoints() {
  console.log('🚀 Test de tous les endpoints...');
  
  const endpoints = [
    {
      url: 'http://localhost:8000/api/v1/users/?role=student',
      description: 'Liste des étudiants (BadgeAwardWidget)'
    },
    {
      url: 'http://localhost:8000/api/v1/badges/',
      description: 'Liste des badges (BadgeAwardWidget)'
    },
    {
      url: 'http://localhost:8000/api/v1/analytics/dashboard/overview',
      description: 'Dashboard Overview (OverviewWidget)'
    },
    {
      url: 'http://localhost:8000/api/v1/gamification/user/stats',
      description: 'Stats Gamification (AdvancedGamificationWidget)'
    },
    {
      url: 'http://localhost:8000/api/v1/gamification/leaderboard?leaderboard_type=global',
      description: 'Leaderboard (AdvancedGamificationWidget)'
    },
    {
      url: 'http://localhost:8000/api/v1/ai/analyze-student/1',
      description: 'AI Analysis (AdvancedAIWidget)',
      method: 'POST'
    }
  ];
  
  let successCount = 0;
  let totalCount = endpoints.length;
  
  for (const endpoint of endpoints) {
    const success = await testAPI(endpoint.url, endpoint.description);
    if (success) successCount++;
  }
  
  console.log(`\n📊 Résumé: ${successCount}/${totalCount} endpoints fonctionnels`);
  
  if (successCount === totalCount) {
    console.log('🎉 Tous les widgets sont corrigés !');
  } else {
    console.log('⚠️ Certains widgets ont encore des problèmes');
  }
}

// Créer les boutons
function createTestButtons() {
  const container = document.createElement('div');
  container.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; background: white; padding: 10px; border: 2px solid #333; border-radius: 5px; font-family: Arial; box-shadow: 0 4px 8px rgba(0,0,0,0.3);';
  
  const title = document.createElement('h3');
  title.textContent = '🧪 Test Widgets';
  title.style.margin = '0 0 10px 0';
  container.appendChild(title);
  
  const btn1 = document.createElement('button');
  btn1.textContent = '🧪 Tester Tous';
  btn1.onclick = testAllEndpoints;
  btn1.style.cssText = 'display: block; margin: 5px 0; padding: 8px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer;';
  container.appendChild(btn1);
  
  const btn2 = document.createElement('button');
  btn2.textContent = '📊 État Token';
  btn2.onclick = () => {
    const token = localStorage.getItem('najah_token');
    const user = localStorage.getItem('najah_user');
    console.log('Token:', token ? '✅ Présent' : '❌ Absent');
    console.log('User:', user ? '✅ Présent' : '❌ Absent');
    if (user) console.log('User data:', JSON.parse(user));
  };
  btn2.style.cssText = 'display: block; margin: 5px 0; padding: 8px; background: #28a745; color: white; border: none; border-radius: 3px; cursor: pointer;';
  container.appendChild(btn2);
  
  document.body.appendChild(container);
}

// Exécuter
console.log('✅ Script de test chargé');
createTestButtons(); 