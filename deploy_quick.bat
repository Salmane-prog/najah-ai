@echo off
echo 🚀 DÉPLOIEMENT RAPIDE NAJAH AI
echo ================================

echo.
echo 📋 Vérification des prérequis...
echo.

REM Vérifier Git
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Git n'est pas installé. Veuillez installer Git d'abord.
    pause
    exit /b 1
)
echo ✅ Git installé

REM Vérifier Node.js
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Node.js n'est pas installé. Veuillez installer Node.js d'abord.
    pause
    exit /b 1
)
echo ✅ Node.js installé

REM Vérifier Python
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python n'est pas installé. Veuillez installer Python d'abord.
    pause
    exit /b 1
)
echo ✅ Python installé

echo.
echo 🎯 Options de déploiement disponibles:
echo.
echo 1. Vercel + Railway (Recommandé - Gratuit)
echo 2. Netlify + Render (Gratuit avec limitations)
echo 3. Heroku (Payant - 7€/mois)
echo 4. DigitalOcean (Payant - 12€/mois)
echo 5. Docker Local
echo.
set /p choice="Choisissez une option (1-5): "

if "%choice%"=="1" goto vercel_railway
if "%choice%"=="2" goto netlify_render
if "%choice%"=="3" goto heroku
if "%choice%"=="4" goto digitalocean
if "%choice%"=="5" goto docker_local
goto invalid_choice

:vercel_railway
echo.
echo 🚀 Déploiement Vercel + Railway
echo ================================
echo.
echo 1. Préparation du repository GitHub...
echo.
set /p github_url="Entrez l'URL de votre repository GitHub: "
if "%github_url%"=="" (
    echo ❌ URL GitHub requise
    pause
    exit /b 1
)

echo.
echo 📝 Instructions pour Vercel (Frontend):
echo.
echo 1. Allez sur https://vercel.com
echo 2. Connectez-vous avec GitHub
echo 3. Cliquez sur "New Project"
echo 4. Sélectionnez votre repository: %github_url%
echo 5. Configuration:
echo    - Framework Preset: Next.js
echo    - Root Directory: frontend
echo    - Build Command: npm run build
echo 6. Variables d'environnement:
echo    - NEXT_PUBLIC_API_URL: https://votre-backend.railway.app
echo.
echo 📝 Instructions pour Railway (Backend):
echo.
echo 1. Allez sur https://railway.app
echo 2. Connectez-vous avec GitHub
echo 3. Cliquez sur "New Project"
echo 4. Sélectionnez "Deploy from GitHub repo"
echo 5. Choisissez votre repository: %github_url%
echo 6. Root Directory: backend
echo 7. Ajoutez PostgreSQL dans Railway
echo 8. Variables d'environnement:
echo    - DATABASE_URL: (automatique avec PostgreSQL)
echo    - SECRET_KEY: votre-secret-key-32-caracteres
echo    - JWT_SECRET_KEY: votre-jwt-secret-key-32-caracteres
echo    - CORS_ORIGINS: https://votre-frontend.vercel.app
echo.
echo ✅ Déploiement configuré! Suivez les instructions ci-dessus.
goto end

:netlify_render
echo.
echo 🚀 Déploiement Netlify + Render
echo ================================
echo.
echo 📝 Instructions pour Netlify (Frontend):
echo.
echo 1. Allez sur https://netlify.com
echo 2. "New site from Git"
echo 3. Sélectionnez GitHub et votre repository
echo 4. Configuration:
echo    - Base directory: frontend
echo    - Build command: npm run build
echo    - Publish directory: frontend/.next
echo.
echo 📝 Instructions pour Render (Backend):
echo.
echo 1. Allez sur https://render.com
echo 2. "New Web Service"
echo 3. Connectez GitHub
echo 4. Configuration:
echo    - Environment: Python 3
echo    - Build Command: pip install -r requirements.txt
echo    - Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT
echo.
goto end

:heroku
echo.
echo 🚀 Déploiement Heroku
echo =====================
echo.
echo ⚠️  Heroku nécessite une carte de crédit (7€/mois minimum)
echo.
set /p continue="Continuer? (y/n): "
if /i not "%continue%"=="y" goto end

echo.
echo 1. Installation de Heroku CLI...
echo Téléchargez depuis: https://devcenter.heroku.com/articles/heroku-cli
echo.
echo 2. Une fois Heroku CLI installé, exécutez:
echo    heroku login
echo    heroku create najah-ai-app
echo    heroku addons:create heroku-postgresql:hobby-dev
echo    git push heroku main
echo.
goto end

:digitalocean
echo.
echo 🚀 Déploiement DigitalOcean
echo ===========================
echo.
echo ⚠️  DigitalOcean nécessite une carte de crédit (12€/mois minimum)
echo.
set /p continue="Continuer? (y/n): "
if /i not "%continue%"=="y" goto end

echo.
echo 📝 Instructions pour DigitalOcean:
echo.
echo 1. Allez sur https://cloud.digitalocean.com
echo 2. "Create App"
echo 3. Connectez GitHub
echo 4. Configuration:
echo    - Backend Service: Python, dossier backend
echo    - Frontend Service: Node.js, dossier frontend
echo    - Database: PostgreSQL
echo.
goto end

:docker_local
echo.
echo 🐳 Déploiement Docker Local
echo ===========================
echo.
echo Installation de Docker Desktop...
echo Téléchargez depuis: https://www.docker.com/products/docker-desktop
echo.
echo Une fois Docker installé, exécutez:
echo    docker-compose up --build
echo.
goto end

:invalid_choice
echo.
echo ❌ Choix invalide. Veuillez choisir entre 1 et 5.
pause
goto :eof

:end
echo.
echo 🎉 Guide de déploiement terminé!
echo.
echo 📚 Pour plus de détails, consultez le fichier DEPLOYMENT_GUIDE.md
echo.
pause
