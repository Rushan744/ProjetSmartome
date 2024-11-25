import pandas as pd

# Use the on_bad_lines argument to skip bad lines
data = pd.read_csv('Export_Conso_Tours Habitat_2024__2024-05-09_16h11.csv', on_bad_lines='skip')

# Check the first few rows of the data
print(data.head())
