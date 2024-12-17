Projet : Pipeline de Données Météo du Sénégal
Description

Ce projet permet de récupérer quotidiennement les données météorologiques de Dakar et Thiès via l'API OpenWeather. Les données récupérées (température, description, pression, humidité, horodatage) sont ensuite stockées dans une base de données PostgreSQL.
Tâches

    Récupérer les données météo : Scraper les données météo de Dakar et Thiès.
    Stocker dans PostgreSQL : Insérer les données dans une base de données PostgreSQL.
    Docker : Créer un fichier docker-compose.yml pour exécuter l'application et la base de données PostgreSQL dans des conteneurs Docker.
    Hébergement sur GitHub : Héberger le code sur GitHub.
    Visualisation : Utiliser Power BI ou Looker Studio pour visualiser les données.

Prérequis

    Docker et Docker Compose installés.
    Clé API d'OpenWeather.


Créez un fichier .env avec les informations suivantes :

API_KEY=VotreCléAPI
DB_NAME=Weather
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432

Construisez et lancez les services Docker :

    docker-compose up --build

    Accédez à la base de données PostgreSQL sur localhost:5434.

Structure des fichiers

projet-pipeline-meteo/
├── app.py                # Code principal
├── requirements.txt      # Dépendances Python
├── wait-for-it.sh        # Script pour attendre PostgreSQL
├── docker-compose.yml    # Configuration Docker
├── Dockerfile   # Dockerfile pour l'application
├── .init.sql         
├── .env                  # Fichier de configuration des variables d'environnement

Base de données

La table weather_data contient les informations météo :

CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    ville VARCHAR(50),
    temperature FLOAT,
    description VARCHAR(255),
    pression INT,
    humidite INT,
    horodatage TIMESTAMP
);
