from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import psycopg2
import requests
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Configuration de la base de données et de l'API
API_KEY = os.getenv("API_KEY")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITIES = ["Dakar", "Thies", "Saint-Louis", "Ziguinchor", "Kaolack"]

def fetch_weather(city):
    """Récupérer les données météo pour une ville donnée."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        return {
            "ville": data["name"],
            "température": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "pression": data["main"]["pressure"],
            "humidité": data["main"]["humidity"],
            "horodatage": datetime.utcfromtimestamp(data["dt"]).strftime('%Y-%m-%d %H:%M:%S')
        }
    except requests.exceptions.RequestException as e:
        print(f"Erreur réseau pour {city}: {e}")
    except KeyError as e:
        print(f"Donnée manquante dans la réponse API pour {city}: {e}")
    return None

def save_to_db(weather_data):
    """Insérer les données météo dans PostgreSQL."""
    try:
        with psycopg2.connect(**DB_CONFIG) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO weather_data (ville, temperature, description, pression, humidite, horodatage)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    weather_data["ville"],
                    weather_data["température"],
                    weather_data["description"],
                    weather_data["pression"],
                    weather_data["humidité"],
                    weather_data["horodatage"]
                ))
                conn.commit()
                print(f"Données insérées pour {weather_data['ville']}.")
    except psycopg2.Error as e:
        print(f"Erreur PostgreSQL : {e}")

def run_scraping():
    for city in CITIES:
        weather = fetch_weather(city)
        if weather:
            save_to_db(weather)

# Définir le DAG Airflow
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'start_date': datetime(2024, 12, 22),
}

with DAG(
    'weather_scraping_dag',
    default_args=default_args,
    description='DAG pour le scraping des données météorologiques',
    schedule_interval='@daily',
) as dag:
    scrape_task = PythonOperator(
        task_id='scrape_weather',
        python_callable=run_scraping
    )
