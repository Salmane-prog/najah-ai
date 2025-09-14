#!/usr/bin/env pwsh
<#
.SYNOPSIS
    🎯 Script de démarrage du système d'évaluation initiale NAJAH AI
    
.DESCRIPTION
    Ce script vérifie l'environnement, teste le système et démarre le serveur
    d'évaluation initiale pour les étudiants.
    
.PARAMETER SkipTest
    Ignore le test rapide du système
    
.PARAMETER Port
    Port sur lequel démarrer le serveur (défaut: 8000)
    
.EXAMPLE
    .\start_assessment_windows.ps1
    
.EXAMPLE
    .\start_assessment_windows.ps1 -SkipTest -Port 8001
#>

param(
    [switch]$SkipTest,
    [int]$Port = 8000
)

# Configuration de l'encodage pour les emojis
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "🎯 SYSTÈME D'ÉVALUATION INITIALE NAJAH AI" -ForegroundColor Yellow
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Fonction pour afficher les messages avec couleurs
function Write-Status {
    param(
        [string]$Message,
        [string]$Type = "Info"
    )
    
    switch ($Type) {
        "Success" { Write-Host "✅ $Message" -ForegroundColor Green }
        "Warning" { Write-Host "⚠️  $Message" -ForegroundColor Yellow }
        "Error" { Write-Host "❌ $Message" -ForegroundColor Red }
        "Info" { Write-Host "📋 $Message" -ForegroundColor Blue }
        default { Write-Host "$Message" }
    }
}

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "🔧 $Message" -ForegroundColor Magenta
    Write-Host ""
}

# Étape 1: Vérification de l'environnement
Write-Step "Vérification de l'environnement..."

# Vérifier Python
try {
    $pythonVersion = python --version 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Python détecté: $pythonVersion" "Success"
    } else {
        throw "Python non trouvé"
    }
} catch {
    Write-Status "ERREUR: Python n'est pas installé ou n'est pas dans le PATH" "Error"
    Write-Host "   Veuillez installer Python depuis https://python.org" -ForegroundColor Red
    Write-Host ""
    Read-Host "Appuyez sur Entrée pour quitter"
    exit 1
}

# Étape 2: Vérification des dépendances
Write-Step "Vérification des dépendances..."

try {
    python -c "import fastapi, uvicorn, sqlalchemy" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Status "Toutes les dépendances sont installées" "Success"
    } else {
        throw "Dépendances manquantes"
    }
} catch {
    Write-Status "Certains packages ne sont pas installés" "Warning"
    Write-Host "Installation automatique en cours..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        pip install fastapi uvicorn sqlalchemy
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Dépendances installées avec succès" "Success"
        } else {
            throw "Échec de l'installation"
        }
    } catch {
        Write-Status "ERREUR: Impossible d'installer les dépendances" "Error"
        Write-Host "   Vérifiez votre connexion internet et relancez" -ForegroundColor Red
        Write-Host ""
        Read-Host "Appuyez sur Entrée pour quitter"
        exit 1
    }
}

# Étape 3: Vérification de la base de données
Write-Step "Vérification de la base de données..."

$dbPath = "data\app.db"
if (Test-Path $dbPath) {
    Write-Status "Base de données trouvée" "Success"
} else {
    Write-Status "Base de données non trouvée" "Warning"
    Write-Host "Création automatique en cours..." -ForegroundColor Yellow
    Write-Host ""
    
    try {
        python -c "from core.database import engine; from models import Base; Base.metadata.create_all(bind=engine)"
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Base de données créée avec succès" "Success"
        } else {
            throw "Échec de la création"
        }
    } catch {
        Write-Status "ERREUR: Impossible de créer la base de données" "Error"
        Write-Host "   Vérifiez les permissions du dossier" -ForegroundColor Red
        Write-Host ""
        Read-Host "Appuyez sur Entrée pour quitter"
        exit 1
    }
}

# Étape 4: Test rapide du système (optionnel)
if (-not $SkipTest) {
    Write-Step "Test rapide du système..."
    
    try {
        python quick_test.py
        if ($LASTEXITCODE -eq 0) {
            Write-Status "Test rapide réussi" "Success"
        } else {
            Write-Status "Le test rapide a rencontré des problèmes" "Warning"
            Write-Host "   Le serveur peut quand même fonctionner" -ForegroundColor Yellow
            Write-Host ""
            
            $continue = Read-Host "Voulez-vous continuer quand même ? (O/N)"
            if ($continue -notmatch "^[Oo]") {
                Write-Host ""
                Write-Status "Démarrage annulé" "Error"
                Read-Host "Appuyez sur Entrée pour quitter"
                exit 1
            }
        }
    } catch {
        Write-Status "Impossible d'exécuter le test rapide" "Warning"
        Write-Host "   Continuons avec le démarrage du serveur" -ForegroundColor Yellow
    }
}

# Étape 5: Démarrage du serveur
Write-Step "Démarrage du serveur d'évaluation..."

Write-Host "📍 Le serveur sera accessible sur:" -ForegroundColor Cyan
Write-Host "   • API: http://localhost:$Port" -ForegroundColor White
Write-Host "   • Documentation: http://localhost:$Port/docs" -ForegroundColor White
Write-Host "   • Test: http://localhost:$Port/test-assessment" -ForegroundColor White
Write-Host ""
Write-Host "📱 Pour tester le frontend:" -ForegroundColor Cyan
Write-Host "   • Page d'évaluation: http://localhost:3001/dashboard/student/assessment" -ForegroundColor White
Write-Host ""
Write-Host "⚠️  Appuyez sur Ctrl+C pour arrêter le serveur" -ForegroundColor Yellow
Write-Host ""

# Modifier le port dans le script de démarrage si nécessaire
if ($Port -ne 8000) {
    Write-Host "🔄 Modification du port à $Port..." -ForegroundColor Yellow
    
    # Créer une copie temporaire avec le bon port
    $startScript = Get-Content "start_assessment_system.py" -Raw
    $startScript = $startScript -replace "8000", $Port
    $startScript | Out-File "start_assessment_system_temp.py" -Encoding UTF8
    
    try {
        python start_assessment_system_temp.py
    } finally {
        # Nettoyer le fichier temporaire
        if (Test-Path "start_assessment_system_temp.py") {
            Remove-Item "start_assessment_system_temp.py"
        }
    }
} else {
    # Démarrer le serveur avec le port par défaut
    python start_assessment_system.py
}

Write-Host ""
Write-Status "Serveur arrêté" "Info"
Read-Host "Appuyez sur Entrée pour quitter"





