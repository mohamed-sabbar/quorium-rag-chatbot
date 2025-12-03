#!/bin/bash
# Assurez-vous que ce fichier est exécutable : chmod +x docker.sh

# Structure 'case' pour gérer les arguments (build, up, down, ingest, logs)

case "$1" in
    build)
        echo "🏗️ Construction des images Docker pour le backend et le frontend..."
        # Construit les images en lisant les Dockerfiles spécifiés dans docker-compose.yml
        docker-compose build
        ;;

    up)
        echo "🚀 Démarrage des services RAG (Backend et Frontend) en arrière-plan..."
        # Démarre tous les conteneurs définis dans docker-compose.yml en mode détaché (-d)
        docker-compose up -d
        ;;

    down)
        echo "🗑️ Arrêt et suppression des conteneurs et des réseaux..."
        # Arrête et supprime l'environnement de travail
        docker-compose down
        ;;

    ingest)
        echo "📄 Exécution du pipeline d'ingestion (ingest.py)..."
        # Lance le script Python ingest.py dans un conteneur temporaire 'backend'.
        # --rm : Garantit que le conteneur est supprimé immédiatement après l'exécution (bonne pratique).
        # C'est la commande qui crée l'index vectoriel persistant.
        docker-compose run --rm backend python ingest.py
        ;;

    logs)
        echo "📝 Affichage des logs en temps réel pour le débogage (Ctrl+C pour arrêter)..."
        # Affiche les logs de tous les services en mode suiveur (-f)
        docker-compose logs -f
        ;;

    *)
        echo "Usage: ./docker.sh {build|up|down|ingest|logs}"
        exit 1
        ;;
esac