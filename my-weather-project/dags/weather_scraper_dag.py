from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.http.hooks.http import HttpHook
from datetime import datetime
import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Connexions Airflow (Postgres et API)
POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'meteo_api'

# Charger l'API Key depuis les variables d'environnement ou Airflow
API_KEY = os.getenv("API_KEY")

# Liste des villes à scrapper
CITIES = [
    "Dakar", "Thies", "Saint-Louis", "Ziguinchor", "Kaolack", 
    "Tambacounda", "Louga", "Fatick", "Kolda", "Diourbel", "Matam", "Goudomp", "Kédougou"
]

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# Fonction pour récupérer la météo
def fetch_weather(city):
    # Utilisation de HttpHook d'Airflow pour interagir avec l'API
    http_hook = HttpHook(method='GET', http_conn_id=API_CONN_ID)
    params = {"q": city, "appid": API_KEY, "units": "metric", "lang": "fr"}
    response = http_hook.run(endpoint=BASE_URL, params=params)
    
    if response.status_code == 200:
        data = response.json()
        return {
            "ville": data["name"],
            "température": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "pression": data["main"]["pressure"],
            "humidité": data["main"]["humidity"],
            "horodatage": datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')
        }
    else:
        raise Exception(f"Erreur lors de la récupération des données météo pour {city}")

# Fonction pour enregistrer les données dans la base de données
def save_to_db(weather_data):
    # Utilisation de PostgresHook d'Airflow pour interagir avec PostgreSQL
    postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
    sql = """
        INSERT INTO weather_data (ville, temperature, description, pression, humidite, horodatage)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    postgres_hook.run(sql, parameters=(
        weather_data["ville"],
        weather_data["température"],
        weather_data["description"],
        weather_data["pression"],
        weather_data["humidité"],
        weather_data["horodatage"]
    ))

# Fonction principale pour lancer le scraping et l'enregistrement dans la DB
def run_scraping():
    for city in CITIES:
        weather = fetch_weather(city)
        if weather:
            save_to_db(weather)

# Définition du DAG
default_args = {'owner': 'airflow', 'retries': 1, 'start_date': datetime(2024, 12, 22)}

with DAG(
    'weather_scraping_dag',
    default_args=default_args,
    description='DAG pour le scraping des données météorologiques',
    schedule_interval='@daily',  # Remplace schedule_interval par schedule
) as dag:
    scrape_task = PythonOperator(
        task_id='scrape_weather',
        python_callable=run_scraping
    )
