@echo off
chcp 65001 >nul
echo.
echo ========================================
echo 🎯 SYSTÈME D'ÉVALUATION INITIALE NAJAH AI
echo ========================================
echo.

echo 📋 Vérification de l'environnement...
echo.

REM Vérifier si Python est installé
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERREUR: Python n'est pas installé ou n'est pas dans le PATH
    echo    Veuillez installer Python depuis https://python.org
    echo.
    pause
    exit /b 1
)

echo ✅ Python détecté
python --version

echo.
echo 📦 Vérification des dépendances...
echo.

REM Vérifier si les packages requis sont installés
python -c "import fastapi, uvicorn, sqlalchemy" >nul 2>&1
if %errorlevel% neq 0 (
    echo ⚠️  Certains packages ne sont pas installés
    echo    Installation automatique en cours...
    echo.
    pip install fastapi uvicorn sqlalchemy
    if %errorlevel% neq 0 (
        echo ❌ ERREUR: Impossible d'installer les dépendances
        echo    Vérifiez votre connexion internet et relancez
        echo.
        pause
        exit /b 1
    )
    echo ✅ Dépendances installées avec succès
)

echo.
echo 🗄️  Vérification de la base de données...
echo.

REM Vérifier si la base de données existe
if not exist "data\app.db" (
    echo ⚠️  Base de données non trouvée
    echo    Création automatique en cours...
    echo.
    python -c "from core.database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
    if %errorlevel% neq 0 (
        echo ❌ ERREUR: Impossible de créer la base de données
        echo    Vérifiez les permissions du dossier
        echo.
        pause
        exit /b 1
    )
    echo ✅ Base de données créée avec succès
) else (
    echo ✅ Base de données trouvée
)

echo.
echo 🧪 Test rapide du système...
echo.

REM Lancer le test rapide
python quick_test.py
if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Le test rapide a rencontré des problèmes
    echo    Le serveur peut quand même fonctionner
    echo.
    choice /C YN /M "Voulez-vous continuer quand même"
    if %errorlevel% equ 2 (
        echo.
        echo ❌ Démarrage annulé
        pause
        exit /b 1
    )
)

echo.
echo 🚀 Démarrage du serveur d'évaluation...
echo.

echo 📍 Le serveur sera accessible sur:
echo    • API: http://localhost:8000
echo    • Documentation: http://localhost:8000/docs
echo    • Test: http://localhost:8000/test-assessment
echo.
echo 📱 Pour tester le frontend:
echo    • Page d'évaluation: http://localhost:3001/dashboard/student/assessment
echo.
echo ⚠️  Appuyez sur Ctrl+C pour arrêter le serveur
echo.

REM Démarrer le serveur
python start_assessment_system.py

echo.
echo 🛑 Serveur arrêté
pause





