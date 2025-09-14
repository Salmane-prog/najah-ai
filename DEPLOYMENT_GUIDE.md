# 🚀 Guide d'hébergement - Najah AI

## Vue d'ensemble du projet

**Najah AI** est une application full-stack d'analytics éducative avec :
- **Frontend** : Next.js 15.4.1 + React 19.1.0 + TypeScript
- **Backend** : FastAPI + Python
- **Base de données** : SQLite (développement) / PostgreSQL (production)

---

## 🎯 Options d'hébergement recommandées

### 1. **Vercel (Recommandé pour Next.js)**

#### Avantages :
- ✅ Optimisé pour Next.js
- ✅ Déploiement automatique depuis GitHub
- ✅ CDN global gratuit
- ✅ SSL automatique
- ✅ Fonctions serverless

#### Étapes de déploiement :

1. **Préparer le projet :**
   ```bash
   # Dans le dossier frontend
   cd frontend
   npm run build
   ```

2. **Connecter à Vercel :**
   - Aller sur [vercel.com](https://vercel.com)
   - Connecter votre compte GitHub
   - Importer le repository
   - Configurer les variables d'environnement

3. **Variables d'environnement Vercel :**
   ```
   NEXT_PUBLIC_API_URL=https://your-backend-url.com
   ```

#### Coût : Gratuit (limite de bande passante)

---

### 2. **Railway (Recommandé pour full-stack)**

#### Avantages :
- ✅ Support Python et Node.js
- ✅ Base de données PostgreSQL incluse
- ✅ Déploiement automatique
- ✅ Interface simple

#### Étapes de déploiement :

1. **Préparer les fichiers :**
   ```bash
   # Créer un fichier railway.json
   echo '{"build": {"builder": "NIXPACKS"}}' > railway.json
   ```

2. **Déployer :**
   - Aller sur [railway.app](https://railway.app)
   - Connecter GitHub
   - Sélectionner le repository
   - Railway détectera automatiquement la configuration

#### Coût : $5/mois (plan hobby)

---

### 3. **DigitalOcean App Platform**

#### Avantages :
- ✅ Support multi-services
- ✅ Base de données gérée
- ✅ Scaling automatique
- ✅ Monitoring intégré

#### Configuration :

1. **Créer app.yaml :**
   ```yaml
   name: najah-ai
   services:
   - name: frontend
     source_dir: /frontend
     github:
       repo: your-username/najah-ai
       branch: main
     run_command: npm start
     environment_slug: node-js
     instance_count: 1
     instance_size_slug: basic-xxs
     routes:
     - path: /
   
   - name: backend
     source_dir: /backend
     github:
       repo: your-username/najah-ai
       branch: main
     run_command: uvicorn main:app --host 0.0.0.0 --port 8080
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     routes:
     - path: /api
   ```

#### Coût : $12/mois (2 services)

---

### 4. **AWS (Production avancée)**

#### Services recommandés :
- **Frontend** : AWS Amplify ou S3 + CloudFront
- **Backend** : AWS Elastic Beanstalk ou ECS
- **Base de données** : RDS PostgreSQL
- **Storage** : S3 pour les fichiers

#### Coût : $20-50/mois selon l'usage

---

### 5. **Hébergement VPS (Contrôle total)**

#### Fournisseurs recommandés :
- **Hetzner** : €4.15/mois
- **DigitalOcean Droplet** : $6/mois
- **Linode** : $5/mois
- **Vultr** : $6/mois

#### Configuration VPS :

1. **Installer Docker :**
   ```bash
   curl -fsSL https://get.docker.com -o get-docker.sh
   sh get-docker.sh
   ```

2. **Cloner et déployer :**
   ```bash
   git clone https://github.com/your-username/najah-ai.git
   cd najah-ai
   docker-compose up -d
   ```

3. **Configurer Nginx (reverse proxy) :**
   ```nginx
   server {
       listen 80;
       server_name your-domain.com;
       
       location / {
           proxy_pass http://localhost:3000;
       }
       
       location /api {
           proxy_pass http://localhost:8000;
       }
   }
   ```

---

## 🔧 Configuration pour la production

### Variables d'environnement

Créer un fichier `.env.production` :

```env
# Backend
DATABASE_URL=postgresql://user:password@host:port/database
SECRET_KEY=your-secret-key-here
CORS_ORIGINS=https://your-frontend-domain.com

# Frontend
NEXT_PUBLIC_API_URL=https://your-backend-domain.com
NEXT_PUBLIC_APP_NAME=Najah AI
```

### Base de données PostgreSQL

1. **Créer la base de données :**
   ```sql
   CREATE DATABASE najah_ai;
   CREATE USER najah_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE najah_ai TO najah_user;
   ```

2. **Migrer depuis SQLite :**
   ```bash
   # Exporter les données SQLite
   sqlite3 app.db .dump > data.sql
   
   # Importer dans PostgreSQL
   psql -h your-host -U najah_user -d najah_ai -f data.sql
   ```

---

## 🚀 Déploiement rapide (Docker)

### Local avec Docker :
```bash
# Cloner le projet
git clone https://github.com/your-username/najah-ai.git
cd najah-ai

# Démarrer avec Docker Compose
docker-compose up -d

# Accéder à l'application
# Frontend: http://localhost:3000
# Backend: http://localhost:8000
```

### Production avec Docker :
```bash
# Construire les images
docker build -f Dockerfile.frontend -t najah-ai-frontend .
docker build -f Dockerfile.backend -t najah-ai-backend .

# Démarrer en production
docker-compose -f docker-compose.prod.yml up -d
```

---

## 📊 Monitoring et maintenance

### Outils recommandés :
- **Uptime** : UptimeRobot (gratuit)
- **Logs** : Papertrail ou LogDNA
- **Métriques** : New Relic ou DataDog
- **Sauvegardes** : Automatiques avec le provider

### Commandes utiles :
```bash
# Voir les logs
docker-compose logs -f

# Redémarrer les services
docker-compose restart

# Mettre à jour l'application
git pull && docker-compose up -d --build

# Sauvegarder la base de données
docker-compose exec backend pg_dump -U najah_user najah_ai > backup.sql
```

---

## 🎯 Recommandation finale

**Pour commencer rapidement :**
1. **Vercel** pour le frontend (gratuit)
2. **Railway** pour le backend + base de données ($5/mois)

**Pour la production :**
1. **DigitalOcean App Platform** (solution complète)
2. **VPS + Docker** (contrôle total)

**Budget total recommandé :** $5-15/mois pour commencer




