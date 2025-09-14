// Script simple pour corriger l'authentification
console.log('🔧 CORRECTION SIMPLE');

function fixAuth() {
  fetch('http://localhost:8000/api/v1/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      email: 'superadmin@najah.ai',
      password: 'password123'
    })
  })
  .then(r => r.json())
  .then(data => {
    if (data.access_token) {
      localStorage.removeItem('najah_token');
      localStorage.removeItem('najah_user');
      localStorage.setItem('najah_token', data.access_token);
      localStorage.setItem('najah_user', JSON.stringify({
        id: data.id,
        email: 'superadmin@najah.ai',
        name: data.name || 'superadmin',
        role: data.role
      }));
      console.log('✅ Token mis à jour');
      setTimeout(() => window.location.reload(), 1000);
    }
  });
}

const btn = document.createElement('button');
btn.textContent = '🔄 Reconnecter';
btn.style.cssText = 'position: fixed; top: 10px; right: 10px; z-index: 9999; padding: 15px; background: red; color: white; border: none; border-radius: 8px; cursor: pointer;';
btn.onclick = fixAuth;
document.body.appendChild(btn); 