console.log('🔧 DIAGNOSTIC AUTHENTIFICATION PROFESSEUR');

// Fonction pour diagnostiquer l'état actuel
function diagnoseAuth() {
  console.log('📊 État actuel:');
  
  const token = localStorage.getItem('najah_token');
  const user = localStorage.getItem('najah_user');
  
  console.log('Token:', token ? '✅ Présent' : '❌ Absent');
  console.log('User:', user ? '✅ Présent' : '❌ Absent');
  
  if (user) {
    try {
      const userData = JSON.parse(user);
      console.log('User data:', userData);
    } catch (e) {
      console.log('❌ Erreur parsing user data');
    }
  }
  
  if (token) {
    console.log('Token length:', token.length);
    console.log('Token starts with:', token.substring(0, 20) + '...');
  }
}

// Fonction pour se connecter en tant que professeur
async function loginAsTeacher() {
  console.log('👨‍🏫 Connexion en tant que professeur...');
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/auth/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        email: 'teacher@najah.ai',
        password: 'password123'
      })
    });
    
    if (!response.ok) {
      const error = await response.json();
      console.log('❌ Erreur connexion:', error);
      return false;
    }
    
    const data = await response.json();
    console.log('✅ Connexion réussie:', data);
    
    // Stocker les données
    localStorage.setItem('najah_token', data.access_token);
    localStorage.setItem('najah_user', JSON.stringify({
      id: data.id,
      email: 'teacher@najah.ai',
      name: data.name || 'teacher',
      role: data.role
    }));
    
    console.log('💾 Données stockées');
    return true;
  } catch (error) {
    console.log('❌ Erreur:', error);
    return false;
  }
}

// Fonction pour tester une requête API
async function testAPI() {
  console.log('🧪 Test API...');
  
  const token = localStorage.getItem('najah_token');
  if (!token) {
    console.log('❌ Pas de token');
    return;
  }
  
  try {
    const response = await fetch('http://localhost:8000/api/v1/users/?role=student', {
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    });
    
    console.log('Status:', response.status);
    console.log('OK:', response.ok);
    
    if (response.ok) {
      const data = await response.json();
      console.log('✅ Données reçues:', data.length, 'étudiants');
    } else {
      const error = await response.text();
      console.log('❌ Erreur:', error);
    }
  } catch (error) {
    console.log('❌ Erreur réseau:', error);
  }
}

// Fonction pour nettoyer et reconnecter
async function fixAuth() {
  console.log('🔧 Correction authentification...');
  
  // Nettoyer
  localStorage.removeItem('najah_token');
  localStorage.removeItem('najah_user');
  console.log('🧹 localStorage nettoyé');
  
  // Se reconnecter
  const success = await loginAsTeacher();
  if (success) {
    console.log('✅ Authentification corrigée');
    await testAPI();
  } else {
    console.log('❌ Échec de la correction');
  }
}

// Créer les boutons
function createButtons() {
  const container = document.createElement('div');
  container.style.cssText = 'position: fixed; top: 10px; left: 10px; z-index: 9999; background: white; padding: 10px; border: 2px solid #333; border-radius: 5px; font-family: Arial;';
  
  const title = document.createElement('h3');
  title.textContent = '🔧 Auth Teacher';
  title.style.margin = '0 0 10px 0';
  container.appendChild(title);
  
  const btn1 = document.createElement('button');
  btn1.textContent = '📊 Diagnostiquer';
  btn1.onclick = diagnoseAuth;
  btn1.style.cssText = 'display: block; margin: 5px 0; padding: 8px; background: #007bff; color: white; border: none; border-radius: 3px; cursor: pointer;';
  container.appendChild(btn1);
  
  const btn2 = document.createElement('button');
  btn2.textContent = '👨‍🏫 Connecter Teacher';
  btn2.onclick = loginAsTeacher;
  btn2.style.cssText = 'display: block; margin: 5px 0; padding: 8px; background: #28a745; color: white; border: none; border-radius: 3px; cursor: pointer;';
  container.appendChild(btn2);
  
  const btn3 = document.createElement('button');
  btn3.textContent = '🧪 Tester API';
  btn3.onclick = testAPI;
  btn3.style.cssText = 'display: block; margin: 5px 0; padding: 8px; background: #ffc107; color: black; border: none; border-radius: 3px; cursor: pointer;';
  container.appendChild(btn3);
  
  const btn4 = document.createElement('button');
  btn4.textContent = '🔧 Corriger Auth';
  btn4.onclick = fixAuth;
  btn4.style.cssText = 'display: block; margin: 5px 0; padding: 8px; background: #dc3545; color: white; border: none; border-radius: 3px; cursor: pointer;';
  container.appendChild(btn4);
  
  document.body.appendChild(container);
}

// Exécuter
console.log('✅ Script chargé');
diagnoseAuth();
createButtons(); 