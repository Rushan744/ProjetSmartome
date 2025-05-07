import pandas as pd
import numpy as np

from faker import Faker
import pandas as pd
import random
from datetime import datetime, timedelta

# Initialiser Faker
fake = Faker()

# Dictionnaire pour corréler les villes et les codes postaux
city_postal_codes = {
    "Paris": (75001, 75020),
    "Lyon": (69001, 69009),
    "Tours": (37000, 37999),
}

# Génération des données des bâtiments
def generate_buildings_data(num_buildings=6):
    buildings = []
    for _ in range(num_buildings):
        # Sélectionner une ville et son intervalle de codes postaux
        city, postal_range = random.choice(list(city_postal_codes.items()))
        postal_code = random.randint(postal_range[0], postal_range[1])

        # Générer le DPE
        dpe_class = random.choice(["A", "B", "C", "D", "E", "F", "G"])
        dpe_value = {
            "A": random.randint(0, 50),
            "B": random.randint(51, 90),
            "C": random.randint(91, 150),
            "D": random.randint(151, 230),
            "E": random.randint(231, 330),
            "F": random.randint(331, 450),
            "G": random.randint(451, 800),
        }[dpe_class]

        # Générer la surface
        surface_m2 = round(random.uniform(50, 150), 2)
        surface_m3 = round(surface_m2 * 2.5, 2)  # Hauteur moyenne : 2.5 m

        buildings.append({
            "Adresse": fake.street_address(),
            "Code Postal": postal_code,
            "Ville": city,
            "Type d'énergie": random.choice(["Electricity", "Gas", "Solar"]),
            "Année de fabrication": fake.date_between(start_date="-120y", end_date="-2y"),
            "Surface (m²)": surface_m2,
            "Surface (m³)": surface_m3,
            "DPE Classe": dpe_class,
            "DPE Valeur": dpe_value,
            "Orientation": random.choice(["Nord", "Sud", "Est", "Ouest"]),
        })
    return pd.DataFrame(buildings)

# Génération des données de température et de consommation
def generate_temperature_data(building, start_date, end_date, interval):
    data = []
    current_date = start_date
    heating_rate = 1  # Taux d'augmentation par intervalle (°C/30min)
    cooling_rate = 0.5  # Taux de diminution par intervalle (°C/30min)

    current_temp_int = 10  # Température intérieure initiale
    current_temp_ext = 10  # Température extérieure initiale

    while current_date <= end_date:
        hour = current_date.hour
        if 8 <= hour < 20:
            consigne_temp = 19
        else:
            consigne_temp = 10

        # Ajuster la température intérieure
        if current_temp_int < consigne_temp:
            current_temp_int += min(heating_rate, consigne_temp - current_temp_int)
        elif current_temp_int > consigne_temp:
            current_temp_int -= min(cooling_rate, current_temp_int - consigne_temp)

        # Variations aléatoires
        current_temp_int += random.uniform(-0.5, 0.5)

        # Déterminer la température extérieure
        month = current_date.month
        if month in [12, 1, 2]:
            temp_ext_base = random.uniform(-10, 5)
        elif month in [3, 4, 5]:
            temp_ext_base = random.uniform(5, 15)
        elif month in [6, 7, 8]:
            temp_ext_base = random.uniform(15, 30)
        else:
            temp_ext_base = random.uniform(5, 15)

        temp_ext_base += random.uniform(-3, 3)
        current_temp_ext = (current_temp_ext * 0.8) + (temp_ext_base * 0.2)

        # Présence
        presence = 1 if (8 <= hour < 20 or (hour == 20 and random.choice([0, 1]))) else 0

        # Temps de chauffe
        time_heating = 0
        if current_temp_int < consigne_temp:  # Chauffe uniquement si T_int < consigne
            time_heating = max(0, consigne_temp - current_temp_int) #* presence

        # Humidité et ensoleillement
        humidity = random.uniform(30, 90)  # Humidité en %
        sunlight = random.uniform(0, 8) if month in [6, 7, 8] else random.uniform(0, 4)  # Heures d'ensoleillement

        puissance,temps_de_chauffe = tps_de_chauffe(building["Surface (m³)"],round(current_temp_int, 2),round(current_temp_ext, 2),building["DPE Classe"])
        # Ajouter les données
        data.append({
            "Adresse": building["Adresse"],
            "Datetime": current_date,
            "Consigne Température (°C)": round(consigne_temp, 2),
            "Température Intérieure (°C)": round(current_temp_int, 2),
            "Température Extérieure (°C)": round(current_temp_ext, 2),
            "Présence": presence,
            "Temps de Chauffe (°C*min)": round(time_heating * 30, 2),  # Approximativement en minutes
            "Humidité (%)": round(humidity, 2),
            "Ensoleillement (h)": round(sunlight, 2),
            "Orientation": building["Orientation"],
            "DPE Classe": building["DPE Classe"],
            "DPE Valeur": building["DPE Valeur"],
            "Année de fabrication": building["Année de fabrication"],
            "Surface (m²)": building["Surface (m²)"],
            "Surface (m³)": building["Surface (m³)"],
            "Code Postal": building["Code Postal"],
            "Ville": building["Ville"],
            'Puissance': puissance,
            'temps de chauffe':temps_de_chauffe
        })

        # Prochain intervalle
        current_date += interval

    return pd.DataFrame(data)

def tps_de_chauffe(surface,current_temp_int,current_temp_ext,classe_dpe):
    dico_deper={'A':[0.2,0.5],'B':[0.5,0.8],'C':[0.8,1.2],'D':[1.2,1.8],'E':[1.8,2.5],'F':[2.5,3.5],'G':[3.5,5]}
    if classe_dpe in dico_deper:
        k = random.uniform(dico_deper[classe_dpe][0], dico_deper[classe_dpe][1])
    dt=abs(current_temp_int-current_temp_ext)
    if dt!=0:
        chauffe=(surface*dt)/(surface*dt*k*k)
    else:
        chauffe=0
    return surface*dt*k, chauffe


# Génération des datasets combinés
def generate_combined_dataset():
    start_date = datetime(2024, 1, 1)
    end_date = datetime(2025, 1, 1, 1, 30)  # Réduit pour exemple rapide
    interval = timedelta(minutes=30)

    # Générer les bâtiments
    buildings_df = generate_buildings_data(num_buildings=6)

    # Générer les données pour chaque bâtiment
    combined_data = pd.DataFrame()
    for _, building in buildings_df.iterrows():
        building_data = generate_temperature_data(building, start_date, end_date, interval)
        combined_data = pd.concat([combined_data, building_data], ignore_index=True)

    return combined_data

# Générer et sauvegarder les données
try:
    dataset = generate_combined_dataset()
except Exception as e:
    print(f"Erreur lors de la génération du dataset : {e}")

df = dataset.copy()
df.describe()