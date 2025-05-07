import pandas as pd
import streamlit as st
from tinydb import TinyDB
from sklearn.preprocessing import MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

# Load data from TinyDB
db_path = "tinydb_database.json"
db = TinyDB(db_path)
data = db.all()

df = pd.DataFrame(data)

st.title("Building Temperature Prediction")

# Show the dataset
st.subheader("Dataset Preview")
st.write("Displaying first 10 rows of data:")
st.dataframe(df.head(10))

# Step 1: Handle missing data by filling with the median
st.write("Filling missing data with median...")
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
df[numeric_columns] = df[numeric_columns].fillna(df[numeric_columns].median())

# Step 2: Normalize temperature data
st.write("Normalizing temperature data...")
scaler = MinMaxScaler()
df[['Consigne Température (°C)', 'Température Intérieure (°C)', 'Température Extérieure (°C)']] = scaler.fit_transform(
    df[['Consigne Température (°C)', 'Température Intérieure (°C)', 'Température Extérieure (°C)']])

# Step 3: Create a new feature: Temperature Differential (Interior Temp - Exterior Temp)
st.write("Creating temperature differential feature...")
df['Température Différentielle (°C)'] = df['Température Intérieure (°C)'] - df['Température Extérieure (°C)']

# Display processed data
st.subheader("Processed Data Preview")
st.dataframe(df.head(10))

# Step 4: Prepare data for training
target = 'Consigne Température (°C)'
features = ['Température Intérieure (°C)', 'Température Extérieure (°C)', 'Température Différentielle (°C)', 'Surface (m²)', 'Surface (m³)']

X = df[features]
y = df[target]

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Step 5: Train a machine learning model
st.write("Training model...")
model = LinearRegression()
model.fit(X_train, y_train)

# Step 6: Make predictions and evaluate the model
st.write("Evaluating model performance...")
y_pred = model.predict(X_test)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
rmse = mse ** 0.5
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

# Display the model performance metrics
st.subheader("Model Performance:")
st.write(f"RMSE: {rmse:.2f}")
st.write(f"MAE: {mae:.2f}")
st.write(f"R²: {r2:.2f}")


# Add interactive input for predictions
st.subheader("Make a Prediction")
input_data = {}
for feature in features:
    input_data[feature] = st.number_input(f"Enter {feature}", value=float(df[feature].median()))

if st.button("Predict"):
    input_df = pd.DataFrame([input_data])
    prediction = model.predict(input_df)[0]
    st.write(f"Predicted Consigne Température: {prediction:.2f}°C")