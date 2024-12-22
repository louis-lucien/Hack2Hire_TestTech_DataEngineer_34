Projet : Pipeline de Données Météo du Sénégal

Description

Ce projet permet de récupérer quotidiennement les données météorologiques de Dakar et Thiès via l'API OpenWeather. Les données récupérées (température, description, pression, humidité, horodatage) sont ensuite stockées dans une base de données PostgreSQL.

Tâches

Récupérer les données météo : Scraper les données météo de Dakar et Thiès.

Stocker dans PostgreSQL : Insérer les données dans une base de données PostgreSQL.

Docker : Créer un fichier docker-compose.yml pour exécuter l'application et la base de données PostgreSQL dans des conteneurs Docker.

Hébergement sur GitHub : Héberger le code sur GitHub.

Visualisation : Utiliser Power BI ou Looker Studio pour visualiser les données.

Orchestration avec Astro CLI : Automatiser les flux de données avec Astro CLI.

Tableau de bord Streamlit : Créer une interface interactive pour visualiser et analyser les données météo.

Prérequis

Docker et Docker Compose installés.

Clé API d'OpenWeather.

Astro CLI installé.

Streamlit installé.

Configuration de l'environnement

Créez un fichier .env avec les informations suivantes :

API_KEY=VotreCléAPI
DB_NAME=Weather
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=postgres
DB_PORT=5432

Lancer le projet avec Docker

Construisez et lancez les services Docker :

docker-compose up --build

Accédez à la base de données PostgreSQL sur localhost:5434.

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

Orchestration avec Astro CLI

Installation des dépendances Astro CLI :

astro dev init

Déploiement du pipeline :

astro dev start

Planification des tâches : Définir les DAG pour automatiser l'extraction, le traitement et le stockage des données météo.

Tableau de bord Streamlit

Lancer Streamlit :

streamlit run dashboard.py

Accéder au tableau de bord :
Ouvrez votre navigateur sur http://localhost:8501.

Visualisation

Les données collectées sont affichées via le tableau de bord Streamlit