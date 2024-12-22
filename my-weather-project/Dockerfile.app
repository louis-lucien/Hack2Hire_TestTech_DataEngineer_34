FROM python:3.10

# Installer netcat-openbsd pour le script wait-for-it.sh
RUN apt-get update && apt-get install -y netcat-openbsd

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers nécessaires
COPY app.py .
COPY requirements.txt .
COPY wait-for-it.sh /app/wait-for-it.sh

# Donner les permissions d'exécution au script wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

# Installer les dépendances
RUN pip install --no-cache-dir -r requirements.txt

# Commande par défaut pour attendre PostgreSQL et démarrer l'application
CMD ["/app/wait-for-it.sh", "postgres:5432", "--", "python", "app.py"]
