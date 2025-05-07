'''import streamlit as st
import pandas as pd
import random
from faker import Faker

# Initialize Faker for generating realistic data
faker = Faker()

# Function to generate fake data
def generate_fake_data():
    big_cities = ["Paris", "Lyon", "Tours"]  # Major cities in France
    data = {
        "Adresse": [faker.street_address() for _ in range(3)],  # Random street addresses
        "Code Postal": [random.randint(75000, 95999) for _ in range(3)],  # French postal codes
        "Ville": random.sample(big_cities, 3),  # Ensure different big cities
        "Type d'énergie": [random.choice(["Electricity", "Gas", "Solar"]) for _ in range(3)],  # Random energy types
    }
    return pd.DataFrame(data)

# Streamlit app
st.title("Fake Data Generator")
st.write("### Generate Fake Data for Big Cities in France")

# Generate data when button is clicked
if st.button("Generate Data"):
    fake_data = generate_fake_data()
    st.success("Data generated successfully!")
    
    # Display the generated data
    st.write("### Generated Data")
    st.dataframe(fake_data)
    
    # Add a download button for the data
    csv = fake_data.to_csv(index=False, sep=';').encode('utf-8')
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="realistic_fake_data_with_big_cities.csv",
        mime="text/csv",
    )'''
    
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
        "Type d'énergie": [random.choice(["Electricity", "Gas", "Solar"]) for _ in range(num_rows)],  # Energy types
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

