# Script PowerShell pour redémarrer le backend
Write-Host "🔄 Arrêt des processus Python/Uvicorn..." -ForegroundColor Yellow

# Arrêter tous les processus Python/Uvicorn
Get-Process | Where-Object {$_.ProcessName -like "*python*" -or $_.ProcessName -like "*uvicorn*"} | Stop-Process -Force -ErrorAction SilentlyContinue

Start-Sleep -Seconds 2

Write-Host "🚀 Démarrage du backend..." -ForegroundColor Green

# Démarrer le backend
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload





