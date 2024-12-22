FROM quay.io/astronomer/astro-runtime:12.6.0

FROM python:3.9  # Or any appropriate Python version

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install streamlit  # Ensure streamlit is installed

CMD ["streamlit", "run", "app.py"]  # Start streamlit on app.py or relevant script
