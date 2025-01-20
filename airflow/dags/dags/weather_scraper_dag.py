from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.hooks.http import HttpHook
from datetime import datetime
from dotenv import load_dotenv
from app.app import crawl  # Importer la fonction crawl depuis app/app.py


# Charger les variables d'environnement
load_dotenv()
# Définir le DAG Airflow
with DAG(
    'weather_data_dag',  # Nom du DAG
    default_args={
        'owner': 'airflow',
        'retries': 1,
        'start_date': datetime(2024, 12, 22),  # Date de début du DAG
    },
    description='DAG pour collecter et sauvegarder les données météo',
    schedule_interval='@hourly',  # Exécuter toutes les heures
) as dag:
    # Tâche Airflow pour exécuter la fonction crawl
    weather_data_task = PythonOperator(
        task_id='fetch_weather_data',  # Identifiant de la tâche
        python_callable=crawl  # Appel à la fonction crawl
    )
