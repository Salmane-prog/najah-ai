@echo off
echo 🚀 DÉPLOIEMENT NAJAH AI SUR RAILWAY
echo ====================================

echo.
echo 📦 Installation de Railway CLI...
npm i -g @railway/cli

echo.
echo ✅ Vérification de l'installation...
railway --version

echo.
echo 🔑 Connexion à Railway (navigateur va s'ouvrir)...
railway login

echo.
echo 📁 Initialisation du projet...
railway init

echo.
echo 🗄️ Ajout de PostgreSQL...
railway add postgresql

echo.
echo ⚙️ Configuration des variables d'environnement...
railway variables set SECRET_KEY="najah-ai-secret-2024"
railway variables set JWT_SECRET_KEY="najah-ai-jwt-2024"
railway variables set CORS_ORIGINS="*"
railway variables set PYTHON_ENV="production"

echo.
echo 🚀 Déploiement du backend...
cd backend
railway up

echo.
echo ✅ DÉPLOIEMENT TERMINÉ !
echo 🌐 Votre API sera accessible sur l'URL fournie par Railway
echo 📚 Documentation API : https://votre-url.railway.app/docs

pause

