@echo off
echo 🚀 Script pour uploader le projet Najah AI sur GitHub
echo.

REM Vérifier si Git est installé
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git n'est pas installé. Veuillez l'installer depuis https://git-scm.com/download/win
    pause
    exit /b 1
)

echo ✅ Git est installé
echo.

REM Aller dans le répertoire du projet
cd /d "F:\IMT\stage\Yancode\Najah__AI"

echo 📁 Répertoire actuel: %cd%
echo.

REM Ajouter tous les fichiers
echo 📦 Ajout de tous les fichiers...
git add .

REM Commit
echo 💾 Création du commit...
git commit -m "Upload complete Najah AI project with frontend and backend"

REM Push vers GitHub
echo 🚀 Upload vers GitHub...
git push origin main

echo.
echo ✅ Upload terminé ! Vérifiez votre repository GitHub.
pause

