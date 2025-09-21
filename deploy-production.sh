#!/bin/bash

# Script de déploiement en production pour Najah AI
# Usage: ./deploy-production.sh

set -e

echo "🚀 Déploiement de Najah AI en production..."

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Créer le fichier .env.production s'il n'existe pas
if [ ! -f .env.production ]; then
    echo "📝 Création du fichier .env.production..."
    cat > .env.production << EOF
# Configuration de production
NODE_ENV=production
PYTHON_ENV=production

# Base de données PostgreSQL
DATABASE_URL=postgresql://najah_user:najah_password@postgres:5432/najah_ai

# Sécurité
SECRET_KEY=$(openssl rand -hex 32)
JWT_SECRET_KEY=$(openssl rand -hex 32)
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
CORS_ORIGINS=https://votre-domaine.com,https://www.votre-domaine.com
ALLOWED_HOSTS=votre-domaine.com,www.votre-domaine.com

# Frontend
NEXT_PUBLIC_API_URL=https://votre-domaine.com/api
NEXT_PUBLIC_APP_NAME=Najah AI
NEXT_PUBLIC_APP_VERSION=1.0.0

# Backend
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
BACKEND_WORKERS=4

# PostgreSQL
POSTGRES_DB=najah_ai
POSTGRES_USER=najah_user
POSTGRES_PASSWORD=najah_password

# Uploads
UPLOAD_DIR=./data/uploads
MAX_FILE_SIZE=10485760

# Monitoring
LOG_LEVEL=INFO
EOF
    echo "⚠️  N'oubliez pas de modifier les URLs dans .env.production avec votre domaine !"
fi

# Arrêter les conteneurs existants
echo "🛑 Arrêt des conteneurs existants..."
docker-compose -f docker-compose.prod.yml down || true

# Construire les images
echo "🔨 Construction des images Docker..."
docker-compose -f docker-compose.prod.yml build --no-cache

# Démarrer les services
echo "🚀 Démarrage des services..."
docker-compose -f docker-compose.prod.yml up -d

# Attendre que les services soient prêts
echo "⏳ Attente du démarrage des services..."
sleep 30

# Vérifier le statut des services
echo "📊 Vérification du statut des services..."
docker-compose -f docker-compose.prod.yml ps

# Afficher les logs
echo "📋 Logs des services:"
docker-compose -f docker-compose.prod.yml logs --tail=50

echo "✅ Déploiement terminé !"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:8000"
echo "📚 Documentation API: http://localhost:8000/docs"
echo ""
echo "📝 Pour voir les logs en temps réel:"
echo "   docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "🛑 Pour arrêter les services:"
echo "   docker-compose -f docker-compose.prod.yml down"

