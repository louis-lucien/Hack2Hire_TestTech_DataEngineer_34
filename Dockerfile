
FROM python:3.10

# DÃ©finir le rÃ©pertoire de travail dans le conteneur

WORKDIR /app

# Copier les fichiers nÃ©cessaires dans le conteneur

COPY app.py .

COPY requirements.txt .

COPY wait-for-it.sh /app/wait-for-it.sh

# Rendre le script wait-for-it.sh exÃ©cutable

RUN chmod +x /app/wait-for-it.sh

# Installer les dÃ©pendances Python

RUN pip install --no-cache-dir -r requirements.txt
# Commande par dÃ©faut Ã  exÃ©cuter

CMD ["python", "app.py"]
