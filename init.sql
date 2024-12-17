CREATE TABLE IF NOT EXISTS weather_data (
    id SERIAL PRIMARY KEY,
    ville VARCHAR(50),
    temperature FLOAT,
    description VARCHAR(255),
    pression INT,
    humidite INT,
    horodatage TIMESTAMP
);
