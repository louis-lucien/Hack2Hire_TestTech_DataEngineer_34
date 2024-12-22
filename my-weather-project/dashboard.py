import streamlit as st
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Connexion à PostgreSQL
def get_data_from_postgres():
    conn = psycopg2.connect(
        host="postgres",
        port="5432",
        dbname="Weaher",  # Remplacez par le nom de votre base de données
        user="postgres",    # Remplacez par votre utilisateur
        password="postgres"  # Remplacez par votre mot de passe
    )
    query = "SELECT * FROM weather_data;"  # Remplacez par votre requête ou table
    df = pd.read_sql(query, conn)
    conn.close()
    return df

# Configuration du tableau de bord Streamlit
st.set_page_config(
    page_title="Dashboard Météorologique",
    layout="wide",  # Pour une mise en page large
    initial_sidebar_state="expanded"  # La barre latérale ouverte par défaut
)

# Titre principal
st.title("Tableau de Bord Météorologique Professionnel")
st.markdown("""
Bienvenue sur le tableau de bord interactif des données météorologiques. 
Vous pouvez explorer les informations relatives aux conditions météorologiques telles que la température, l'humidité, la vitesse du vent, et bien plus encore.
""")

# Récupérer les données de la base de données
df = get_data_from_postgres()

# Ajouter un filtre sur les régions ou dates (si nécessaire)
region = st.sidebar.selectbox("Sélectionner la région", df['region'].unique())
filtered_data = df[df['region'] == region]

# Afficher un aperçu des données
st.subheader(f"Aperçu des données pour {region}")
st.write(filtered_data)

# Section pour les visualisations
st.subheader("Visualisations des données météorologiques")

# Graphique 1 : Température moyenne par jour
st.write("### Température Moyenne par Jour")
temp_fig = px.line(filtered_data, x='date', y='temperature', title='Température Moyenne au Fil du Temps')
st.plotly_chart(temp_fig)

# Graphique 2 : Humidité moyenne par jour
st.write("### Humidité Moyenne par Jour")
humidity_fig = px.line(filtered_data, x='date', y='humidity', title='Humidité Moyenne au Fil du Temps')
st.plotly_chart(humidity_fig)

# Graphique 3 : Température vs Humidité (Scatter Plot)
st.write("### Température vs Humidité")
scatter_fig = px.scatter(filtered_data, x='temperature', y='humidity', title='Relation Température - Humidité')
st.plotly_chart(scatter_fig)

# Graphique 4 : Distribution des températures
st.write("### Distribution des Températures")
sns.set(style="whitegrid")
plt.figure(figsize=(10, 6))
sns.histplot(filtered_data['temperature'], kde=True, color="blue", bins=20)
st.pyplot(plt)

# Ajouter des sections interactives avec les utilisateurs
st.sidebar.header("Filtres et Options")

# Sélectionner une période de temps pour afficher les données
start_date = st.sidebar.date_input("Date de début", pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("Date de fin", pd.to_datetime("2023-12-31"))

filtered_data_time = filtered_data[(filtered_data['date'] >= start_date) & (filtered_data['date'] <= end_date)]

st.write(f"### Données filtrées entre {start_date} et {end_date}")
st.write(filtered_data_time)

# Graphique de température sur la période sélectionnée
time_fig = px.line(filtered_data_time, x='date', y='temperature', title='Température sur la Période Sélectionnée')
st.plotly_chart(time_fig)

# Enregistrement des données filtrées ou visualisation
st.sidebar.download_button(
    label="Télécharger les Données",
    data=filtered_data_time.to_csv(),
    file_name="weather_data_filtered.csv",
    mime="text/csv"
)
