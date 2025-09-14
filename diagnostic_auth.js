// Script de diagnostic complet pour l'authentification
console.log('🔍 DIAGNOSTIC COMPLET DE L\'AUTHENTIFICATION');
console.log('=============================================');

// 1. Vérifier le localStorage
const user = localStorage.getItem('najah_user');
const token = localStorage.getItem('najah_token');

console.log('\n📋 1. ÉTAT DU LOCALSTORAGE:');
console.log('- Utilisateur:', user ? JSON.parse(user) : '❌ Non trouvé');
console.log('- Token:', token ? token.substring(0, 50) + '...' : '❌ Non trouvé');

// 2. Vérifier si le token est valide
if (token) {
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    console.log('\n🔐 2. ANALYSE DU TOKEN:');
    console.log('- Expiration:', new Date(payload.exp * 1000));
    console.log('- Utilisateur:', payload.sub);
    console.log('- Rôle:', payload.role);
    
    const now = new Date();
    const exp = new Date(payload.exp * 1000);
    
    if (exp < now) {
      console.log('❌ Token expiré!');
    } else {
      console.log('✅ Token valide');
    }
  } catch (error) {
    console.log('❌ Erreur lors du décodage du token:', error);
  }
} else {
  console.log('\n❌ 2. AUCUN TOKEN TROUVÉ');
}

// 3. Tester une requête API simple
console.log('\n🌐 3. TEST D\'UNE REQUÊTE API:');
if (token) {
  fetch('/api/v1/users/?role=student', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    console.log('- Status:', response.status);
    console.log('- OK:', response.ok);
    if (response.ok) {
      return response.json();
    } else {
      throw new Error(`HTTP ${response.status}`);
    }
  })
  .then(data => {
    console.log('✅ Requête API réussie');
    console.log('- Données reçues:', data.length, 'éléments');
  })
  .catch(error => {
    console.log('❌ Erreur API:', error.message);
  });
} else {
  console.log('❌ Impossible de tester l\'API sans token');
}

// 4. Fonctions de correction
console.log('\n🔧 4. FONCTIONS DE CORRECTION:');

// Fonction pour nettoyer l'authentification
function clearAuth() {
  console.log('🧹 Nettoyage de l\'authentification...');
  localStorage.removeItem('najah_user');
  localStorage.removeItem('najah_token');
  console.log('✅ Authentification nettoyée');
}

// Fonction pour se reconnecter
function reconnect() {
  console.log('🔄 Redirection vers la page de connexion...');
  clearAuth();
  window.location.href = '/login';
}

// Fonction pour tester la connexion
function testLogin() {
  console.log('🧪 Test de connexion...');
  const testData = {
    email: 'superadmin@najah.ai',
    password: 'password123'
  };
  
  fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(testData)
  })
  .then(response => response.json())
  .then(data => {
    if (data.access_token) {
      console.log('✅ Connexion réussie');
      console.log('- Token:', data.access_token.substring(0, 50) + '...');
      console.log('- Rôle:', data.role);
      
      // Stocker le token
      localStorage.setItem('najah_token', data.access_token);
      localStorage.setItem('najah_user', JSON.stringify({
        id: data.id,
        email: testData.email,
        name: data.name || '',
        role: data.role
      }));
      
      console.log('💾 Token stocké dans localStorage');
      console.log('🔄 Rechargement de la page...');
      setTimeout(() => window.location.reload(), 1000);
    } else {
      console.log('❌ Échec de la connexion:', data);
    }
  })
  .catch(error => {
    console.log('❌ Erreur de connexion:', error);
  });
}

// 5. Ajouter des boutons d'action
console.log('\n🎛️ 5. BOUTONS D\'ACTION:');

// Bouton de nettoyage
const clearButton = document.createElement('button');
clearButton.textContent = '🧹 Nettoyer Auth';
clearButton.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 10px; background: orange; color: white; border: none; border-radius: 5px; cursor: pointer; margin-right: 120px;';
clearButton.onclick = clearAuth;
document.body.appendChild(clearButton);

// Bouton de reconnexion
const reconnectButton = document.createElement('button');
reconnectButton.textContent = '🔄 Se reconnecter';
reconnectButton.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 10px; background: red; color: white; border: none; border-radius: 5px; cursor: pointer; margin-right: 60px;';
reconnectButton.onclick = reconnect;
document.body.appendChild(reconnectButton);

// Bouton de test de connexion
const testButton = document.createElement('button');
testButton.textContent = '🧪 Test Connexion';
testButton.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 10px; background: green; color: white; border: none; border-radius: 5px; cursor: pointer;';
testButton.onclick = testLogin;
document.body.appendChild(testButton);

console.log('✅ Boutons ajoutés en haut à droite');
console.log('\n📝 INSTRUCTIONS:');
console.log('1. Cliquez sur "🧪 Test Connexion" pour tester la connexion');
console.log('2. Si ça marche, la page se rechargera automatiquement');
console.log('3. Sinon, cliquez sur "🔄 Se reconnecter" pour aller à /login');
console.log('4. Ou cliquez sur "🧹 Nettoyer Auth" pour nettoyer le localStorage'); 