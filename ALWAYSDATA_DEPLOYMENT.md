# 🚀 Déploiement sur AlwaysData

## Vue d'ensemble
AlwaysData est **parfait** pour votre projet Najah AI car il supporte :
- ✅ Next.js (Frontend)
- ✅ FastAPI (Backend Python)
- ✅ PostgreSQL (Base de données)
- ✅ SSH et contrôle total

## 📋 Plans AlwaysData recommandés

### **Plan Pro** (Recommandé)
- **Prix** : €9.99/mois
- **RAM** : 1GB
- **CPU** : 1 vCore
- **Stockage** : 10GB SSD
- **Bases de données** : PostgreSQL incluse

### **Plan Business** (Pour la production)
- **Prix** : €19.99/mois
- **RAM** : 2GB
- **CPU** : 2 vCores
- **Stockage** : 20GB SSD
- **Bases de données** : PostgreSQL + Redis

## 🔧 Configuration étape par étape

### 1. Créer le compte AlwaysData
1. Aller sur [alwaysdata.com](https://www.alwaysdata.com)
2. Choisir le plan Pro ou Business
3. Créer un compte et valider l'email

### 2. Configuration de la base de données
```sql
-- Dans l'interface AlwaysData > Bases de données
-- Créer une base PostgreSQL
CREATE DATABASE najah_ai;
CREATE USER najah_user WITH PASSWORD 'secure_password';
GRANT ALL PRIVILEGES ON DATABASE najah_ai TO najah_user;
```

### 3. Configuration du Backend FastAPI

#### A. Connexion SSH
```bash
ssh your-username@ssh-alwaysdata.com
```

#### B. Créer la structure
```bash
mkdir -p ~/najah-ai/backend
cd ~/najah-ai/backend
```

#### C. Installer les dépendances Python
```bash
# Créer un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# Installer les dépendances
pip install fastapi uvicorn sqlalchemy psycopg2-binary python-dotenv
```

#### D. Configuration du site web
Dans l'interface AlwaysData :
1. **Sites web** > **Ajouter un site**
2. **Type** : Programme utilisateur
3. **Commande** : `~/najah-ai/backend/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000`
4. **Répertoire** : `~/najah-ai/backend`

### 4. Configuration du Frontend Next.js

#### A. Installer Node.js
```bash
# AlwaysData a Node.js pré-installé
node --version
npm --version
```

#### B. Créer le frontend
```bash
cd ~/najah-ai
# Copier vos fichiers frontend ici
```

#### C. Configuration Next.js
```bash
cd frontend
npm install
npm run build
```

#### D. Configuration du site web
Dans l'interface AlwaysData :
1. **Sites web** > **Ajouter un site**
2. **Type** : Programme utilisateur
3. **Commande** : `~/najah-ai/frontend/node_modules/.bin/next start -p 3000`
4. **Répertoire** : `~/najah-ai/frontend`

### 5. Configuration des variables d'environnement

#### A. Fichier .env pour le backend
```bash
cat > ~/najah-ai/backend/.env << EOF
DATABASE_URL=postgresql://najah_user:secure_password@postgresql-alwaysdata.com:5432/najah_ai
SECRET_KEY=your-super-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
CORS_ORIGINS=https://your-domain.alwaysdata.net
PYTHON_ENV=production
EOF
```

#### B. Fichier .env.local pour le frontend
```bash
cat > ~/najah-ai/frontend/.env.local << EOF
NEXT_PUBLIC_API_URL=https://your-domain.alwaysdata.net/api
NEXT_PUBLIC_APP_NAME=Najah AI
NODE_ENV=production
EOF
```

### 6. Configuration du reverse proxy

#### A. Créer le fichier nginx.conf
```bash
cat > ~/najah-ai/nginx.conf << 'EOF'
server {
    listen 80;
    server_name your-domain.alwaysdata.net;

    # Frontend Next.js
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

### 7. Script de déploiement automatique

```bash
cat > ~/najah-ai/deploy.sh << 'EOF'
#!/bin/bash

echo "🚀 Déploiement sur AlwaysData..."

# Aller dans le répertoire du projet
cd ~/najah-ai

# Mettre à jour le code (si depuis Git)
# git pull origin main

# Backend
echo "🔧 Configuration du backend..."
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
echo "🎨 Configuration du frontend..."
cd ../frontend
npm install
npm run build

# Redémarrer les services
echo "🔄 Redémarrage des services..."
# Les services se redémarrent automatiquement via AlwaysData

echo "✅ Déploiement terminé!"
echo "🌐 Frontend: https://your-domain.alwaysdata.net"
echo "🔧 Backend: https://your-domain.alwaysdata.net/api"
EOF

chmod +x ~/najah-ai/deploy.sh
```

## 🔒 Configuration SSL

AlwaysData fournit automatiquement un certificat SSL gratuit :
1. **Sites web** > Votre site > **SSL**
2. Activer **Let's Encrypt**
3. Votre site sera accessible en HTTPS

## 📊 Monitoring et logs

### Voir les logs
```bash
# Logs du backend
tail -f ~/logs/your-backend-site.log

# Logs du frontend
tail -f ~/logs/your-frontend-site.log
```

### Vérifier le statut
```bash
# Vérifier que les services tournent
ps aux | grep uvicorn
ps aux | grep next
```

## 💰 Coût total

- **Plan Pro** : €9.99/mois
- **Domaine personnalisé** : €0 (inclus)
- **SSL** : €0 (Let's Encrypt gratuit)
- **PostgreSQL** : €0 (inclus)
- **Total** : **€9.99/mois**

## ✅ Avantages AlwaysData

1. **Support complet** de votre stack technologique
2. **Interface d'administration** intuitive
3. **SSH** pour contrôle total
4. **PostgreSQL** incluse
5. **SSL gratuit**
6. **Support français**
7. **Prix compétitif**

## ⚠️ Limitations

1. **Pas de Docker** (mais pas nécessaire)
2. **Configuration manuelle** requise
3. **Pas de scaling automatique**

## 🎯 Recommandation

**AlwaysData est parfait** pour votre projet Najah AI car :
- ✅ Supporte toutes vos technologies
- ✅ Prix très compétitif (€9.99/mois)
- ✅ Interface française
- ✅ Support PostgreSQL inclus
- ✅ SSL gratuit

**Alternative** : Si vous voulez plus de simplicité, Railway reste plus facile à configurer.







