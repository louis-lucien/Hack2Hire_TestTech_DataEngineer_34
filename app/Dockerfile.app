FROM python:3.10

WORKDIR /app

COPY . /app
COPY requirements.txt .

RUN apt-get update && apt-get install -y netcat-openbsd
RUN pip install --no-cache-dir -r requirements.txt

COPY wait-for-it.sh /app/wait-for-it.sh
RUN chmod +x /app/wait-for-it.sh

CMD ["./wait-for-it.sh", "postgres:5432", "--", "python", "app.py"]
