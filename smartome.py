import pandas as pd
import re

def clean_data_with_regex(file_path):
    # Load the data
    data = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

    # Function to clean 'Valeur' column using regex (remove any non-numeric characters)
    def clean_value(value):
        # Using regex to remove any characters that are not digits or decimal point
        return re.sub(r'[^0-9.,-]', '', str(value))

    # Clean 'Valeur' column using the function
    data['Valeur'] = data['Valeur'].apply(clean_value)

    # Fill any missing values with a default value, like 0
    data['Valeur'] = data['Valeur'].fillna(0)

    # Save the cleaned data
    cleaned_file_path = f"cleaned_{file_path.split('/')[-1]}"
    data.to_csv(cleaned_file_path, index=False, sep=';')
    print(f"Cleaned data saved to '{cleaned_file_path}'")

# Example usage
file_paths = [
    "Export_AIH_2024-10-10_12h08.csv",
    "Export_Conso_Tours Habitat_2023_2024-05-09_16h13.csv",
    "Export_Conso_Tours Habitat_2024__2024-05-09_16h11.csv",
    "export_data_2024-11-24_21h15.csv",
    "Export_Data_Val de Roland_2024-05-09_15h49.csv"
]

# Clean each dataset
for file_path in file_paths:
    clean_data_with_regex(file_path)
