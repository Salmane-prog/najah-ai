// Script pour tester et corriger l'authentification
console.log('🔧 TEST ET CORRECTION AUTHENTIFICATION');

function testAuth() {
  console.log('🧪 Test de l\'authentification...');
  
  const token = localStorage.getItem('najah_token');
  const user = localStorage.getItem('najah_user');
  
  console.log('Token:', token ? token.substring(0, 30) + '...' : '❌ Non trouvé');
  console.log('User:', user ? JSON.parse(user) : '❌ Non trouvé');
  
  if (!token) {
    console.log('❌ Pas de token, reconnexion nécessaire');
    reconnect();
    return;
  }
  
  // Tester une requête simple
  fetch('/api/v1/users/?role=student', {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json'
    }
  })
  .then(response => {
    console.log('Status:', response.status);
    if (response.ok) {
      return response.json();
    } else {
      throw new Error(`HTTP ${response.status}`);
    }
  })
  .then(data => {
    console.log('✅ Requête réussie, données:', data.length, 'étudiants');
  })
  .catch(error => {
    console.log('❌ Erreur:', error.message);
    console.log('🔄 Tentative de reconnexion...');
    reconnect();
  });
}

function reconnect() {
  console.log('🔄 Reconnexion en cours...');
  
  fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'superadmin@najah.ai',
      password: 'password123'
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.access_token) {
      console.log('✅ Nouveau token obtenu');
      
      // Nettoyer l'ancien token
      localStorage.removeItem('najah_token');
      localStorage.removeItem('najah_user');
      
      // Stocker le nouveau token
      localStorage.setItem('najah_token', data.access_token);
      localStorage.setItem('najah_user', JSON.stringify({
        id: data.id,
        email: 'superadmin@najah.ai',
        name: data.name || 'superadmin',
        role: data.role
      }));
      
      console.log('💾 Token mis à jour');
      console.log('🔄 Rechargement de la page...');
      
      setTimeout(() => {
        window.location.reload();
      }, 1000);
      
    } else {
      console.log('❌ Échec de la connexion:', data);
    }
  })
  .catch(error => {
    console.log('❌ Erreur de connexion:', error);
  });
}

// Créer les boutons
const testButton = document.createElement('button');
testButton.textContent = '🧪 Test Auth';
testButton.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 15px; background: #4CAF50; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.2); margin-right: 150px;';
testButton.onclick = testAuth;
document.body.appendChild(testButton);

const reconnectButton = document.createElement('button');
reconnectButton.textContent = '🔄 Reconnecter';
reconnectButton.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 15px; background: #ff6b6b; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.2);';
reconnectButton.onclick = reconnect;
document.body.appendChild(reconnectButton);

console.log('✅ Boutons ajoutés');
console.log('📝 Cliquez sur "🧪 Test Auth" pour tester, ou "🔄 Reconnecter" pour reconnexion directe'); 