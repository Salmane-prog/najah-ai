# 🚀 Guide de Déploiement Complet - Najah AI

## 📋 Vue d'ensemble

Ce guide vous explique comment déployer votre application **Najah AI** sur différentes plateformes. Votre projet est une application full-stack avec :
- **Frontend** : Next.js 15.4.1 + TypeScript + Tailwind CSS
- **Backend** : FastAPI + SQLAlchemy + PostgreSQL
- **Base de données** : PostgreSQL (production)

## 🎯 Options de Déploiement

### 1. **Vercel + Railway** (Recommandé) ⭐

#### Pourquoi cette combinaison ?
- ✅ **Gratuit** pour les projets open source
- ✅ **Déploiement automatique** depuis GitHub
- ✅ **Performance optimale** pour Next.js
- ✅ **Base de données PostgreSQL** incluse

#### Déploiement Frontend (Vercel)

1. **Préparer le repository GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/votre-username/najah-ai.git
   git push -u origin main
   ```

2. **Connecter à Vercel**
   - Aller sur [vercel.com](https://vercel.com)
   - Se connecter avec GitHub
   - Cliquer sur "New Project"
   - Sélectionner votre repository
   - Configurer :
     - **Framework Preset** : Next.js
     - **Root Directory** : `frontend`
     - **Build Command** : `npm run build`
     - **Output Directory** : `.next`

3. **Variables d'environnement sur Vercel**
   ```
   NEXT_PUBLIC_API_URL=https://votre-backend-railway.railway.app
   NEXT_PUBLIC_APP_NAME=Najah AI
   ```

#### Déploiement Backend (Railway)

1. **Préparer le backend**
   ```bash
   cd backend
   # S'assurer que railway.json est présent
   ```

2. **Connecter à Railway**
   - Aller sur [railway.app](https://railway.app)
   - Se connecter avec GitHub
   - Cliquer sur "New Project"
   - Sélectionner "Deploy from GitHub repo"
   - Choisir votre repository
   - Configurer le dossier racine : `backend`

3. **Ajouter PostgreSQL**
   - Dans Railway, cliquer sur "New"
   - Sélectionner "Database" → "PostgreSQL"
   - Railway créera automatiquement les variables d'environnement

4. **Variables d'environnement sur Railway**
   ```
   DATABASE_URL=postgresql://user:password@host:port/database
   SECRET_KEY=your-secret-key-here
   JWT_SECRET_KEY=your-jwt-secret-key
   CORS_ORIGINS=https://votre-frontend.vercel.app
   PYTHON_ENV=production
   ```

### 2. **Netlify + Render**

#### Frontend sur Netlify

1. **Connecter à Netlify**
   - Aller sur [netlify.com](https://netlify.com)
   - "New site from Git"
   - Sélectionner GitHub et votre repository

2. **Configuration Build**
   ```
   Base directory: frontend
   Build command: npm run build
   Publish directory: frontend/.next
   ```

#### Backend sur Render

1. **Connecter à Render**
   - Aller sur [render.com](https://render.com)
   - "New Web Service"
   - Connecter GitHub

2. **Configuration**
   ```
   Environment: Python 3
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
   ```

### 3. **Heroku** (Payant)

#### Déploiement complet sur Heroku

1. **Installation Heroku CLI**
   ```bash
   # Windows
   winget install Heroku.HerokuCLI
   
   # Ou télécharger depuis heroku.com
   ```

2. **Préparer les fichiers**
   ```bash
   # Créer Procfile dans le dossier racine
   echo "web: cd backend && uvicorn main:app --host 0.0.0.0 --port \$PORT" > Procfile
   ```

3. **Déployer**
   ```bash
   heroku login
   heroku create najah-ai-app
   heroku addons:create heroku-postgresql:hobby-dev
   git push heroku main
   ```

### 4. **DigitalOcean App Platform**

1. **Créer l'application**
   - Aller sur [cloud.digitalocean.com](https://cloud.digitalocean.com)
   - "Create App"
   - Connecter GitHub

2. **Configuration**
   - **Backend Service** : Python, dossier `backend`
   - **Frontend Service** : Node.js, dossier `frontend`
   - **Database** : PostgreSQL

### 5. **Déploiement Local avec Docker**

1. **Créer Dockerfile**
   ```dockerfile
   # Backend Dockerfile
   FROM python:3.11-slim
   WORKDIR /app
   COPY backend/requirements.txt .
   RUN pip install -r requirements.txt
   COPY backend/ .
   CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
   ```

2. **Docker Compose**
   ```yaml
   version: '3.8'
   services:
     backend:
       build: .
       ports:
         - "8000:8000"
       environment:
         - DATABASE_URL=postgresql://user:pass@db:5432/najah_ai
       depends_on:
         - db
     
     frontend:
       build: ./frontend
       ports:
         - "3000:3000"
       environment:
         - NEXT_PUBLIC_API_URL=http://localhost:8000
     
     db:
       image: postgres:15
       environment:
         - POSTGRES_DB=najah_ai
         - POSTGRES_USER=user
         - POSTGRES_PASSWORD=pass
       volumes:
         - postgres_data:/var/lib/postgresql/data

   volumes:
     postgres_data:
   ```

## 🔧 Configuration Avancée

### Variables d'Environnement Essentielles

#### Backend
```env
# Base de données
DATABASE_URL=postgresql://user:password@host:port/database

# Sécurité
SECRET_KEY=your-secret-key-min-32-chars
JWT_SECRET_KEY=your-jwt-secret-key-min-32-chars

# CORS
CORS_ORIGINS=https://votre-frontend.vercel.app,http://localhost:3000

# Environnement
PYTHON_ENV=production
DEBUG=False
```

#### Frontend
```env
# API
NEXT_PUBLIC_API_URL=https://votre-backend.railway.app

# Application
NEXT_PUBLIC_APP_NAME=Najah AI
NEXT_PUBLIC_APP_VERSION=1.0.0

# Mode
NODE_ENV=production
```

### Optimisations de Performance

1. **Frontend (Next.js)**
   ```javascript
   // next.config.js
   module.exports = {
     output: 'standalone',
     images: {
       domains: ['votre-backend.railway.app'],
     },
     compress: true,
   }
   ```

2. **Backend (FastAPI)**
   ```python
   # main.py
   from fastapi.middleware.gzip import GZipMiddleware
   
   app.add_middleware(GZipMiddleware, minimum_size=1000)
   ```

## 🚨 Dépannage

### Problèmes Courants

1. **Erreur CORS**
   ```python
   # backend/main.py
   app.add_middleware(
       CORSMiddleware,
       allow_origins=["https://votre-frontend.vercel.app"],
       allow_credentials=True,
       allow_methods=["*"],
       allow_headers=["*"],
   )
   ```

2. **Erreur de base de données**
   - Vérifier la variable `DATABASE_URL`
   - S'assurer que PostgreSQL est accessible
   - Vérifier les migrations Alembic

3. **Erreur de build frontend**
   ```bash
   cd frontend
   npm install
   npm run build
   ```

### Logs et Monitoring

1. **Railway**
   - Aller dans l'onglet "Deployments"
   - Cliquer sur les logs

2. **Vercel**
   - Aller dans l'onglet "Functions"
   - Voir les logs de déploiement

## 📊 Coûts Estimés

| Plateforme | Gratuit | Payant |
|------------|---------|--------|
| **Vercel + Railway** | ✅ Illimité | 0€/mois |
| **Netlify + Render** | ✅ Limité | 7-20€/mois |
| **Heroku** | ❌ | 7€/mois minimum |
| **DigitalOcean** | ❌ | 12€/mois minimum |
| **AWS/GCP** | ❌ | Variable |

## 🎯 Recommandation Finale

**Pour votre projet Najah AI, je recommande Vercel + Railway** car :
- ✅ **100% gratuit** pour les projets open source
- ✅ **Déploiement automatique** depuis GitHub
- ✅ **Performance optimale** pour Next.js et FastAPI
- ✅ **Base de données PostgreSQL** incluse
- ✅ **Support excellent** et documentation complète

## 🚀 Prochaines Étapes

1. **Choisir votre plateforme** (Vercel + Railway recommandé)
2. **Préparer votre repository GitHub**
3. **Suivre le guide de déploiement** correspondant
4. **Configurer les variables d'environnement**
5. **Tester votre application déployée**

---

**Besoin d'aide ?** N'hésitez pas à me demander des clarifications sur n'importe quelle étape !