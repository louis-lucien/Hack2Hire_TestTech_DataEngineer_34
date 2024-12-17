import os
import psycopg2
import requests
from datetime import datetime

# Configuration depuis les variables d'environnement
API_KEY = os.getenv("API_KEY")
DB_CONFIG = {
    "dbname": os.getenv("DB_NAME"),  # Nom de la base de données
    "user": os.getenv("DB_USER"),    # Utilisateur PostgreSQL
    "password": os.getenv("DB_PASSWORD"),  # Mot de passe de l'utilisateur
    "host": os.getenv("DB_HOST"),    # Hôte de la base de données (par exemple, 'postgres')
    "port": os.getenv("DB_PORT")     # Port PostgreSQL (par défaut, 5432)
}


BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
CITIES = ["Dakar", "Thies"]

def fetch_weather(city):
    """Récupérer les données météo pour une ville donnée."""
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",
        "lang": "fr"
    }
    response = requests.get(BASE_URL, params=params)
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
    print(f"Erreur pour {city}: {response.status_code}")
    return None

def save_to_db(weather_data):
    """Insérer les données météo dans PostgreSQL."""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()
        insert_query = """
            INSERT INTO weather_data (ville, temperature, description, pression, humidite, horodatage)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (
            weather_data["ville"],
            weather_data["température"],
            weather_data["description"],
            weather_data["pression"],
            weather_data["humidité"],
            weather_data["horodatage"]
        )
        cur.execute(insert_query, values)
        conn.commit()
        cur.close()
        conn.close()
        print(f"Données insérées pour {weather_data['ville']}.")
    except Exception as e:
        print("Erreur d'insertion dans la base :", e)

if __name__ == "__main__":
    for city in CITIES:
        print(f"Récupération des données pour {city}...")
        weather = fetch_weather(city)
        if weather:
            save_to_db(weather)
