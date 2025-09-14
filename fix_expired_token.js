// Script pour corriger le token expiré
console.log('🔧 CORRECTION DU TOKEN EXPIRÉ');

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
      
      // Recharger la page après 1 seconde
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

// Créer le bouton
const button = document.createElement('button');
button.textContent = '🔄 Reconnecter';
button.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 15px; background: #ff6b6b; color: white; border: none; border-radius: 8px; cursor: pointer; font-size: 16px; font-weight: bold; box-shadow: 0 4px 8px rgba(0,0,0,0.2);';
button.onclick = reconnect;
document.body.appendChild(button);

console.log('✅ Bouton de reconnexion ajouté');
console.log('📝 Cliquez sur le bouton rouge pour obtenir un nouveau token'); 