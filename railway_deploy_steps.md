# 🚀 DÉPLOIEMENT NAJAH AI SUR RAILWAY VIA CLI

## Étapes détaillées :

### 1. Se connecter à Railway
```bash
railway login
```
- Cela ouvrira votre navigateur
- Connectez-vous avec votre compte Railway

### 2. Initialiser le projet
```bash
railway init
```
- Choisir "Create new project"
- Nom du projet : "najah-ai"

### 3. Ajouter PostgreSQL
```bash
railway add postgresql
```
- Cela créera automatiquement une base PostgreSQL
- Railway générera l'URL de connexion automatiquement

### 4. Configurer les variables d'environnement
```bash
railway variables set SECRET_KEY="najah-ai-secret-key-2024"
railway variables set JWT_SECRET_KEY="najah-ai-jwt-secret-key-2024"
railway variables set CORS_ORIGINS="*"
railway variables set PYTHON_ENV="production"
```

### 5. Déployer le backend
```bash
cd backend
railway up
```
- Railway va automatiquement :
  - Détecter Python/FastAPI
  - Installer les dépendances depuis requirements.txt
  - Démarrer l'application
  - Créer l'URL publique

### 6. Obtenir l'URL de votre API
```bash
railway status
```
- Copier l'URL publique (ex: https://najah-ai-production.railway.app)

## ✅ Résultat attendu :
- Backend déployé et accessible
- Base PostgreSQL connectée
- API documentation sur : https://votre-url.railway.app/docs
- Données importées automatiquement au premier démarrage

