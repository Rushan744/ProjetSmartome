import streamlit as st
from script import TinyDB, Query
import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# Initialize the TinyDB database
db = TinyDB('db.json')

# Initialize the Query object for querying the database
Record = Query()

# Streamlit UI
st.title("TinyDB Streamlit Application with Data Preprocessing")
st.sidebar.title("Options")

# Sidebar with different options
option = st.sidebar.radio("Choose an Option", ("View Records", "Add Record", "Data Preprocessing", "Visualize Data"))

# View all records
if option == "View Records":
    st.subheader("All Records")
    records = db.all()  # Fetch all records from the database
    if records:
        st.write(records)
    else:
        st.write("No records found in the database.")

# Add a new record
elif option == "Add Record":
    st.subheader("Add New Record")
    
    adresse = st.text_input("Adresse")
    datetime = st.text_input("Datetime")
    temperature = st.number_input("Consigne Température (°C)", min_value=-50, max_value=50)
    interior_temp = st.number_input("Température Intérieure (°C)", min_value=-50, max_value=50)
    exterior_temp = st.number_input("Température Extérieure (°C)", min_value=-50, max_value=50)

    # Add the record to TinyDB
    if st.button("Add Record"):
        new_record = {
            "Adresse": adresse,
            "Datetime": datetime,
            "Consigne Température (°C)": temperature,
            "Température Intérieure (°C)": interior_temp,
            "Température Extérieure (°C)": exterior_temp,
            "Présence": 0,  # Default value
            "Temps de Chauffe (°C*min)": 0.0,  # Default value
            "Humidité (%)": 0.0,  # Default value
            "Ensoleillement (h)": 0.0,  # Default value
            "Orientation": "Ouest",  # Default value
            "DPE Classe": "C",  # Default value
            "DPE Valeur": 146,  # Default value
            "Année de fabrication": "2006-10-19",  # Default value
            "Surface (m²)": 0.0,  # Default value
            "Surface (m³)": 0.0  # Default value
        }
        db.insert(new_record)
        st.success("Record added successfully!")

# Data Preprocessing: Cleaning, Imputing, Normalizing, and Creating Features
elif option == "Data Preprocessing":
    st.subheader("Data Preprocessing")
    
    # Convert TinyDB records to a Pandas DataFrame
    records = db.all()
    if records:
        df = pd.DataFrame(records)
        
        # Step 1: Handle missing data
        if st.checkbox("Fill missing data"):
            st.write("Filling missing values with median...")
            df.fillna(df.median(), inplace=True)
            st.write(df.head())
        
        # Step 2: Normalize the data
        if st.checkbox("Normalize data"):
            st.write("Normalizing temperature data...")
            scaler = MinMaxScaler()
            # Normalize the columns you want (for example, temperature columns)
            df[['Consigne Température (°C)', 'Température Intérieure (°C)', 'Température Extérieure (°C)']] = scaler.fit_transform(
                df[['Consigne Température (°C)', 'Température Intérieure (°C)', 'Température Extérieure (°C)']])
            st.write(df.head())
        
        # Step 3: Feature Creation (e.g., Temperature Differential)
        if st.checkbox("Create temperature differential feature"):
            st.write("Creating temperature differential feature...")
            df['Température Différentielle (°C)'] = df['Température Intérieure (°C)'] - df['Température Extérieure (°C)']
            st.write(df.head())
        
        # Display the processed data
        st.write("Processed Data:")
        st.write(df)

# Visualize data using Seaborn
elif option == "Visualize Data":
    st.subheader("Visualize Data")
    
    # Convert TinyDB records to a Pandas DataFrame
    records = db.all()
    if records:
        df = pd.DataFrame(records)
        
        # Example: Plot Temperature Data using Seaborn
        if 'Consigne Température (°C)' in df.columns:
            st.write("Temperature Distribution:")
            sns.histplot(df['Consigne Température (°C)'], kde=True)
            st.pyplot()
        else:
            st.write("No relevant data to visualize.")
    else:
        st.write("No records found for visualization.")
