'''# Your existing code remains unchanged
import pandas as pd  # Import pandas for working with data
import random  # Import random for generating random values
from datetime import datetime, timedelta  # Import datetime and timedelta for date manipulations

# Define the date range for the data generation
start_date = datetime(2023, 1, 1)  # Start date: January 1, 2023
end_date = datetime(2023, 12, 31)  # End date: December 31, 2023
hours_per_day = 24  # Number of hourly observations per day
num_days = (end_date - start_date).days + 1  # Total number of days in the range

# Generate timestamps for every hour within the date range
timestamps = [start_date + timedelta(hours=i) for i in range(num_days * hours_per_day)]

# Initialize the data dictionary with required fields
data = {
    "Date": [ts.date() for ts in timestamps],  # Extract date from each timestamp
    "Heure": [ts.time() for ts in timestamps],  # Extract time from each timestamp
    "Température extérieure (°C)": [round(random.uniform(-5, 30), 1) for _ in timestamps],  # Random outdoor temperatures
    "Température intérieure actuelle (°C)": [],  # Placeholder for indoor temperature
    "Température cible souhaitée (°C)": [],  # Placeholder for target temperature
    "Consommation énergétique (kWh)": [],  # Placeholder for energy consumption
    "Statut de l'occupation (binaire)": [random.choice([0, 1]) for _ in timestamps],  # Random occupancy (0 or 1)
    "Adresse": [f"Address {i+1}" for i in range(len(timestamps))],  # Generate fake addresses
    "Code Postal": [random.randint(10000, 99999) for _ in timestamps],  # Generate random French-style postal codes
    "Type d'énergie": [random.choice(["Electricity", "Gas", "Solar"]) for _ in timestamps],  # Random energy type
}

# Calculate derived fields based on the occupancy status
for i, occupied in enumerate(data["Statut de l'occupation (binaire)"]):
    if occupied:  # If the unit is occupied
        data["Température cible souhaitée (°C)"].append(22)  # Target temperature is 22°C
        data["Température intérieure actuelle (°C)"].append(round(random.uniform(21, 23), 1))  # Indoor temp near target
        data["Consommation énergétique (kWh)"].append(round(random.uniform(1.5, 3.0), 2))  # Higher energy usage
    else:  # If the unit is unoccupied
        data["Température cible souhaitée (°C)"].append(12)  # Target temperature is 12°C
        data["Température intérieure actuelle (°C)"].append(round(random.uniform(10, 13), 1))  # Indoor temp near target
        data["Consommation énergétique (kWh)"].append(round(random.uniform(0.1, 0.5), 2))  # Lower energy usage

# Convert the data dictionary to a pandas DataFrame
fake_data = pd.DataFrame(data)

# Save the generated data to a CSV file
fake_data.to_csv("fake_residence_data.csv", index=False, sep=';')  # Save with semicolon as delimiter

# Preview the first 5 rows of the dataset
print(fake_data.head())

# Add Streamlit for displaying the data
import streamlit as st  # Import Streamlit for creating the app

# Streamlit App
st.title("Fake Residence Data Viewer")
st.write("### Full Generated Data")

# Display the entire dataset in Streamlit
st.dataframe(fake_data)  # Show the entire dataset in a scrollable table

# Add a download button for the CSV file
csv = fake_data.to_csv(index=False, sep=';').encode('utf-8')
st.download_button(
    label="Download Fake Data as CSV",
    data=csv,
    file_name="fake_residence_data.csv",
    mime="text/csv",
)
'''

from faker import Faker

# Initialiser Faker
fake = Faker()

# Définir les intervalles de DPE en fonction d'une variable
def generate_dpe(category):
    if category == "bad":
        return [fake.random_int(min=450, max=800) for _ in range(2)]
    elif category == "medium":
        return [fake.random_int(min=201, max=449) for _ in range(2)]
    elif category == "good":
        return [fake.random_int(min=0, max=200) for _ in range(2)]
    else:
        return []

# Générer les valeurs DPE selon la catégorie
category = "bad"  # Peut être "bad", "medium", ou "good"
dpe_values = generate_dpe(category)

# Affichage des résultats
print(f"Valeurs DPE ({category.capitalize()}):", dpe_values)

from faker import Faker
import random
from datetime import datetime, timedelta

# Initialiser Faker
fake = Faker()

def generate_humidity(date: datetime, temperature: float) -> float:
    """
    Génère une humidité cohérente en fonction de la date, de l'heure et de la température.
    """
    # Base d'humidité par saison
    if 3 <= date.month <= 5:  # Printemps
        base_humidity = 50
    elif 6 <= date.month <= 8:  # Été
        base_humidity = 40
    elif 9 <= date.month <= 11:  # Automne
        base_humidity = 60
    else:  # Hiver (Décembre, Janvier, Février)
        base_humidity = 70

    # Ajustement selon l'heure
    if 6 <= date.hour <= 18:  # Journée
        time_adjustment = random.uniform(-5, 5)  # Variation plus faible
    else:  # Nuit (plus humide)
        time_adjustment = random.uniform(5, 15)

    # Ajustement selon la température
    if temperature < 5:  # Froid, humidité plus élevée
        temp_adjustment = random.uniform(10, 20)
    elif 5 <= temperature <= 25:  # Température modérée
        temp_adjustment = random.uniform(-5, 5)
    else:  # Chaud, humidité plus basse
        temp_adjustment = random.uniform(-15, -5)

    # Calcul final de l'humidité
    humidity = base_humidity + time_adjustment + temp_adjustment
    return max(0, min(100, round(humidity)))  # Limiter entre 0% et 100%


# Exemple : générer des humidités pour des dates, heures et températures
sample_data = []
start_date = datetime(2025, 1, 1, 0, 0)
for i in range(24 * 30):  # 30 jours avec une mesure toutes les heures
    current_date = start_date + timedelta(hours=i)
    temperature = random.uniform(-5, 35)  # Température aléatoire en °C
    humidity = generate_humidity(current_date, temperature)
    sample_data.append({"date": current_date, "temperature": temperature, "humidity": humidity})

# Afficher quelques exemples
print("\nExemples générés :")
for entry in sample_data[:10]:  # Afficher les 10 premiers
    print(f"Date : {entry['date']}, Température : {entry['temperature']:.1f}°C, Humidité : {entry['humidity']}%")

import pandas as pd
from faker import Faker
import random

# Initialize Faker
faker = Faker()

# Function to generate fake data
def generate_fake_data(num_rows=10):
    # Generate fake data for the specified number of rows
    fake_data = {
        "Adresse": [faker.street_address() for _ in range(num_rows)],
        "Code Postal": [random.randint(75000, 95999) for _ in range(num_rows)],  # French postal codes
        "Ville": [random.choice(["Paris", "Lyon", "Tours"]) for _ in range(num_rows)],  # Big French cities
        "Type d'énergie": [random.choice(["Electricity", "Gas"]) for _ in range(num_rows)],  # Energy types
    }
    # Convert to a DataFrame
    return pd.DataFrame(fake_data)

# Generate fake data
num_rows = 10  # Set the number of rows you want
fake_data_df = generate_fake_data(num_rows)

# Save the generated data to a CSV file
fake_data_df.to_csv("generated_fake_data.csv", index=False, sep=';')

# Print the generated data
print("Fake data generated successfully!")
print(fake_data_df)