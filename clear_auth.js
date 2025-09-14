// Script pour nettoyer l'authentification et revenir à la page d'accueil
console.log('🧹 Nettoyage de l\'authentification...');

// Fonction pour nettoyer le localStorage
function clearAuth() {
  localStorage.removeItem('najah_user');
  localStorage.removeItem('najah_token');
  console.log('✅ Authentification nettoyée');
  console.log('🔄 Redirection vers la page d\'accueil...');
  window.location.href = '/';
}

// Fonction pour vérifier l'état actuel
function checkAuthStatus() {
  const user = localStorage.getItem('najah_user');
  const token = localStorage.getItem('najah_token');
  
  console.log('📊 État actuel de l\'authentification:');
  console.log('  - Utilisateur:', user ? 'Connecté' : 'Non connecté');
  console.log('  - Token:', token ? 'Présent' : 'Absent');
  
  if (user) {
    try {
      const userData = JSON.parse(user);
      console.log('  - Détails utilisateur:', userData);
    } catch (e) {
      console.log('  - Erreur parsing utilisateur');
    }
  }
}

// Exécuter les vérifications
checkAuthStatus();

// Proposer le nettoyage
console.log('\n🎯 Pour nettoyer l\'authentification et revenir à la page d\'accueil:');
console.log('1. Ouvrez la console du navigateur (F12)');
console.log('2. Exécutez: clearAuth()');
console.log('3. Ou cliquez sur le bouton ci-dessous');

// Créer un bouton dans la page
if (typeof document !== 'undefined') {
  const button = document.createElement('button');
  button.textContent = '🧹 Nettoyer l\'authentification';
  button.style.cssText = `
    position: fixed;
    top: 20px;
    right: 20px;
    z-index: 9999;
    background: #ef4444;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    font-size: 14px;
  `;
  button.onclick = clearAuth;
  document.body.appendChild(button);
  
  console.log('🔘 Bouton de nettoyage ajouté à la page');
}

// Exposer la fonction globalement
if (typeof window !== 'undefined') {
  window.clearAuth = clearAuth;
  window.checkAuthStatus = checkAuthStatus;
} 