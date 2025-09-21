# 🚀 Déploiement sur Hostinger VPS

## Prérequis
- VPS Hostinger (Ubuntu 20.04+ recommandé)
- Accès SSH
- Domaine configuré (optionnel)

## Étapes de déploiement

### 1. Connexion au VPS
```bash
ssh root@your-vps-ip
```

### 2. Mise à jour du système
```bash
apt update && apt upgrade -y
```

### 3. Installation de Docker
```bash
# Installer Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh

# Installer Docker Compose
curl -L "https://github.com/docker/compose/releases/download/v2.20.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose

# Vérifier l'installation
docker --version
docker-compose --version
```

### 4. Installation de Git
```bash
apt install git -y
```

### 5. Cloner le projet
```bash
git clone https://github.com/your-username/najah-ai.git
cd najah-ai
```

### 6. Configuration des variables d'environnement
```bash
cp env.example .env
nano .env
```

Modifier les valeurs :
```env
NODE_ENV=production
DATABASE_URL=postgresql://najah_user:najah_password@postgres:5432/najah_ai
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=https://your-domain.com,http://your-vps-ip
NEXT_PUBLIC_API_URL=https://your-domain.com/api
```

### 7. Déploiement avec Docker
```bash
# Démarrer les services
docker-compose -f docker-compose.prod.yml up -d

# Vérifier le statut
docker-compose -f docker-compose.prod.yml ps
```

### 8. Configuration Nginx (si pas de domaine)
```bash
# Installer Nginx
apt install nginx -y

# Créer la configuration
cat > /etc/nginx/sites-available/najah-ai << EOF
server {
    listen 80;
    server_name your-vps-ip;

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
}
EOF

# Activer le site
ln -s /etc/nginx/sites-available/najah-ai /etc/nginx/sites-enabled/
rm /etc/nginx/sites-enabled/default

# Redémarrer Nginx
systemctl restart nginx
systemctl enable nginx
```

### 9. Configuration du pare-feu
```bash
# Installer UFW
apt install ufw -y

# Configurer les règles
ufw allow ssh
ufw allow 80
ufw allow 443
ufw --force enable
```

### 10. Vérification
```bash
# Vérifier que tout fonctionne
curl http://localhost:3000
curl http://localhost:8000/health

# Voir les logs
docker-compose -f docker-compose.prod.yml logs -f
```

## 🔧 Script de déploiement automatique

Créer un script de déploiement :
```bash
cat > deploy-hostinger.sh << 'EOF'
#!/bin/bash

echo "🚀 Déploiement sur Hostinger VPS..."

# Arrêter les services existants
docker-compose -f docker-compose.prod.yml down

# Mettre à jour le code
git pull origin main

# Reconstruire et redémarrer
docker-compose -f docker-compose.prod.yml up -d --build

# Vérifier la santé
sleep 10
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ Déploiement réussi!"
else
    echo "❌ Erreur de déploiement"
    docker-compose -f docker-compose.prod.yml logs
fi
EOF

chmod +x deploy-hostinger.sh
```

## 📊 Monitoring et maintenance

### Commandes utiles
```bash
# Voir les logs
docker-compose -f docker-compose.prod.yml logs -f

# Redémarrer un service
docker-compose -f docker-compose.prod.yml restart frontend

# Mettre à jour
./deploy-hostinger.sh

# Sauvegarder la base de données
docker-compose -f docker-compose.prod.yml exec postgres pg_dump -U najah_user najah_ai > backup.sql

# Voir l'utilisation des ressources
docker stats
```

### Configuration SSL (avec Let's Encrypt)
```bash
# Installer Certbot
apt install certbot python3-certbot-nginx -y

# Obtenir un certificat SSL
certbot --nginx -d your-domain.com

# Vérifier le renouvellement automatique
certbot renew --dry-run
```

## 💰 Coûts estimés

- **VPS Hostinger** : €3.99-7.99/mois
- **Domaine** : €0.99-2.99/mois (optionnel)
- **SSL** : Gratuit (Let's Encrypt)
- **Total** : €4-11/mois

## ⚠️ Limitations Hostinger

1. **Pas de support Docker** sur l'hébergement partagé
2. **VPS requis** pour les applications full-stack
3. **Configuration manuelle** nécessaire
4. **Pas de scaling automatique**

## 🎯 Recommandation

**Hostinger VPS** est une excellente option pour votre projet si :
- Vous voulez un contrôle total
- Vous avez un budget limité
- Vous êtes à l'aise avec la ligne de commande

**Alternative plus simple** : Railway ou DigitalOcean App Platform







