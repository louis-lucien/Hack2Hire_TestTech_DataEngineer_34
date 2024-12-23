import os
import psycopg2
import requests
from datetime import datetime
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Vérification des variables obligatoires
REQUIRED_ENV_VARS = ["API_KEY", "DB_NAME", "DB_USER", "DB_PASSWORD", "DB_HOST", "DB_PORT"]
for var in REQUIRED_ENV_VARS:
    if not os.getenv(var):
        raise EnvironmentError(f"La variable d'environnement {var} est manquante dans le fichier .env.")

# Configuration
API_KEY = os.getenv("API_KEY")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "host": os.getenv("DB_HOST"),
    "port": os.getenv("DB_PORT")
}

BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
# Ajoutez les principales villes/régions du Sénégal
CITIES = [
    "Dakar", "Thies", "Saint-Louis", "Ziguinchor", "Kaolack", 
    "Tambacounda", "Louga", "Fatick", "Kolda", "Diourbel", "Matam", "Goudomp","Kédougou"
]

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

if __name__ == "__main__":
    for city in CITIES:
        print(f"Récupération des données pour {city}...")
        weather = fetch_weather(city)
        if weather:
            save_to_db(weather)
