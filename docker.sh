#!/bin/bash
# Make sure this file is executable: chmod +x docker.sh
# This script provides a simple CLI for managing Docker Compose services
# for the RAG project (backend + frontend).

# Use a 'case' statement to handle different commands:
# build, up, down, ingest, logs

case "$1" in
    build)
        echo " Building Docker images for backend and frontend"
        # Build Docker images as defined in docker-compose.yml
        docker-compose build
        ;;

    up)
        echo "Starting RAG services (Backend and Frontend) in detached mode"
        # Start all services defined in docker-compose.yml in detached mode (-d)
        docker-compose up -d
        ;;

    down)
        echo "topping and removing containers and networks..."
        # Stop and remove all containers and associated networks
        docker-compose down
        ;;

    ingest)
        echo "Running the ingestion pipeline (ingest.py)"
        # Run the ingest.py script inside a temporary backend container
        # --rm ensures the container is deleted after execution
        # This creates the persistent vector store for document embeddings
        docker-compose run --rm backend python ingest.py
        ;;

    logs)
        echo " Displaying real-time logs for debugging (Ctrl+C to stop)."
        # Follow logs of all services (-f for "follow")
        docker-compose logs -f
        ;;

    *)
        echo "Usage: ./docker.sh {build|up|down|ingest|logs}"
        exit 1
        ;;
esac