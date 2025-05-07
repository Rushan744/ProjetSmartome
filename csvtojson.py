import csv
import json

# Read the CSV file with semicolon delimiter
with open('simulation_donnees_batiments.csv', 'r', encoding='utf-8') as csv_file:
    # Create a CSV reader with the correct delimiter
    reader = csv.reader(csv_file, delimiter=';')
    
    # Read the header (first row) and then the data rows
    headers = next(reader)  # First row is the header
    data = []
    
    for row in reader:
        # Create a dictionary using the header and the row data
        row_dict = dict(zip(headers, row))
        data.append(row_dict)

# Write to a JSON file
with open('simulation_donnees_batiments.json', 'w', encoding='utf-8') as json_file:
    json.dump(data, json_file, indent=4)

print("CSV data has been successfully converted to JSON!")
