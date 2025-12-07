<#
.SYNOPSIS
Script Windows pour gérer Docker Compose pour le projet RAG Q&A Chatbot
.PARAMETER cmd
Commande à exécuter : build | up | down | ingest | logs
#>

param(
    [string]$cmd = "up"
)

switch ($cmd) {
    "build" {
        Write-Host "Building Docker images..."
        docker-compose build
    }
    "up" {
        Write-Host "Starting Docker containers..."
        docker-compose up -d
    }
    "down" {
        Write-Host "Stopping Docker containers..."
        docker-compose down
    }
    "ingest" {
        Write-Host "Running document ingestion..."
        docker-compose run --rm backend python ingest.py
    }
    "logs" {
        Write-Host "Tailing logs..."
        docker-compose logs -f
    }
    default {
        Write-Host "Commande non reconnue. Utilisez : build | up | down | ingest | logs"
    }
}
