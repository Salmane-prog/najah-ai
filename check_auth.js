// Script pour vérifier l'état de l'authentification
console.log('🔍 Vérification de l\'authentification...');

// Vérifier le localStorage
const user = localStorage.getItem('najah_user');
const token = localStorage.getItem('najah_token');

console.log('📋 État du localStorage:');
console.log('- Utilisateur:', user ? JSON.parse(user) : 'Non trouvé');
console.log('- Token:', token ? token.substring(0, 50) + '...' : 'Non trouvé');

// Vérifier si le token est valide
if (token) {
  try {
    // Décoder le token JWT (partie payload)
    const payload = JSON.parse(atob(token.split('.')[1]));
    console.log('🔐 Token décodé:');
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
  console.log('❌ Aucun token trouvé');
}

// Fonction pour se reconnecter
function reconnect() {
  console.log('🔄 Tentative de reconnexion...');
  
  // Supprimer les anciens tokens
  localStorage.removeItem('najah_user');
  localStorage.removeItem('najah_token');
  
  // Rediriger vers la page de connexion
  window.location.href = '/login';
}

// Ajouter un bouton de reconnexion si nécessaire
if (!token) {
  const button = document.createElement('button');
  button.textContent = 'Se reconnecter';
  button.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 10px; background: red; color: white; border: none; border-radius: 5px; cursor: pointer;';
  button.onclick = reconnect;
  document.body.appendChild(button);
  
  console.log('🔴 Bouton de reconnexion ajouté');
} 