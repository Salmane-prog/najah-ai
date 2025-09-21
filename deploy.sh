#!/bin/bash

# Script de déploiement pour Najah AI
# Usage: ./deploy.sh [environment]

set -e

ENVIRONMENT=${1:-production}
PROJECT_NAME="najah-ai"

echo "🚀 Déploiement de Najah AI en mode $ENVIRONMENT"

# Vérifier que Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

# Créer le fichier .env s'il n'existe pas
if [ ! -f .env ]; then
    echo "📝 Création du fichier .env depuis env.example"
    cp env.example .env
    echo "⚠️  Veuillez modifier le fichier .env avec vos vraies valeurs avant de continuer"
    exit 1
fi

# Fonction pour arrêter les services
stop_services() {
    echo "🛑 Arrêt des services existants..."
    docker-compose -f docker-compose.yml down 2>/dev/null || true
    docker-compose -f docker-compose.prod.yml down 2>/dev/null || true
}

# Fonction pour nettoyer les images inutilisées
cleanup() {
    echo "🧹 Nettoyage des images Docker inutilisées..."
    docker system prune -f
}

# Fonction pour sauvegarder la base de données
backup_database() {
    if [ "$ENVIRONMENT" = "production" ]; then
        echo "💾 Sauvegarde de la base de données..."
        mkdir -p backup
        docker-compose -f docker-compose.prod.yml exec -T postgres pg_dump -U najah_user najah_ai > backup/backup_$(date +%Y%m%d_%H%M%S).sql
    fi
}

# Fonction pour déployer
deploy() {
    echo "🔨 Construction des images Docker..."
    
    if [ "$ENVIRONMENT" = "production" ]; then
        docker-compose -f docker-compose.prod.yml build --no-cache
        echo "🚀 Démarrage des services en production..."
        docker-compose -f docker-compose.prod.yml up -d
    else
        docker-compose build --no-cache
        echo "🚀 Démarrage des services en développement..."
        docker-compose up -d
    fi
}

# Fonction pour vérifier la santé des services
health_check() {
    echo "🏥 Vérification de la santé des services..."
    
    # Attendre que les services démarrent
    sleep 10
    
    # Vérifier le backend
    if curl -f http://localhost:8000/health > /dev/null 2>&1; then
        echo "✅ Backend est opérationnel"
    else
        echo "❌ Backend n'est pas accessible"
        return 1
    fi
    
    # Vérifier le frontend
    if curl -f http://localhost:3000 > /dev/null 2>&1; then
        echo "✅ Frontend est opérationnel"
    else
        echo "❌ Frontend n'est pas accessible"
        return 1
    fi
}

# Fonction pour afficher les logs
show_logs() {
    echo "📋 Logs des services:"
    if [ "$ENVIRONMENT" = "production" ]; then
        docker-compose -f docker-compose.prod.yml logs --tail=50
    else
        docker-compose logs --tail=50
    fi
}

# Fonction pour afficher les informations de déploiement
show_info() {
    echo ""
    echo "🎉 Déploiement terminé!"
    echo ""
    echo "📱 Frontend: http://localhost:3000"
    echo "🔧 Backend API: http://localhost:8000"
    echo "📚 Documentation API: http://localhost:8000/docs"
    echo "🏥 Health Check: http://localhost:8000/health"
    echo ""
    echo "📋 Commandes utiles:"
    echo "  - Voir les logs: docker-compose logs -f"
    echo "  - Arrêter: docker-compose down"
    echo "  - Redémarrer: docker-compose restart"
    echo "  - Mettre à jour: ./deploy.sh $ENVIRONMENT"
    echo ""
}

# Exécution principale
main() {
    echo "🔍 Vérification de l'environnement..."
    
    # Arrêter les services existants
    stop_services
    
    # Sauvegarder en production
    if [ "$ENVIRONMENT" = "production" ]; then
        backup_database
    fi
    
    # Déployer
    deploy
    
    # Vérifier la santé
    if health_check; then
        show_info
    else
        echo "❌ Échec du déploiement. Vérifiez les logs:"
        show_logs
        exit 1
    fi
    
    # Nettoyer
    cleanup
}

# Gestion des arguments
case "${1:-}" in
    "stop")
        stop_services
        ;;
    "logs")
        show_logs
        ;;
    "restart")
        stop_services
        deploy
        health_check
        ;;
    "backup")
        backup_database
        ;;
    *)
        main
        ;;
esac







