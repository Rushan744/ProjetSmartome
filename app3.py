import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

# Function to load and clean data
def load_and_clean_data(uploaded_file):
    try:
        # Read the dataset with semicolon as delimiter
        data = pd.read_csv(uploaded_file, delimiter=';', on_bad_lines='skip')
        
        # Display success message
        st.success("Dataset loaded successfully!")
        
        # Display the first few rows of the dataset
        st.write("### Dataset Preview")
        st.dataframe(data.head())
        
        # Handle missing values by dropping rows with NaN values
        data_cleaned = data.dropna()
        
        # Try to convert all columns to numeric where applicable
        for col in data_cleaned.columns:
            try:
                data_cleaned[col] = pd.to_numeric(data_cleaned[col], errors='coerce')
            except Exception as e:
                st.warning(f"Skipping column {col} conversion: {e}")
        
        return data_cleaned
        
    except Exception as e:
        st.error(f"Error loading the dataset: {e}")
        st.stop()

# File uploader
uploaded_file = st.file_uploader("Upload your CSV file for visualization", type="csv")

if uploaded_file:
    # Load and clean the data
    data_cleaned = load_and_clean_data(uploaded_file)

    # Visualization options
    st.sidebar.header("Visualization Options")
    x_col = st.sidebar.selectbox("Select X-axis Column", data_cleaned.columns)
    y_col = st.sidebar.selectbox("Select Y-axis Column", data_cleaned.columns)
    plot_type = st.sidebar.radio("Select Plot Type", ["Line", "Bar", "Scatter"])

    # Generate the selected plot
    st.write("### Visualization")
    if plot_type == "Line":
        st.line_chart(data_cleaned.set_index(x_col)[y_col])
    elif plot_type == "Bar":
        st.bar_chart(data_cleaned.set_index(x_col)[y_col])
    elif plot_type == "Scatter":
        fig, ax = plt.subplots()
        ax.scatter(data_cleaned[x_col], data_cleaned[y_col], alpha=0.7)
        ax.set_xlabel(x_col)
        ax.set_ylabel(y_col)
        ax.set_title(f"{plot_type} Plot of {x_col} vs {y_col}")
        st.pyplot(fig)

    # Option to show raw data
    if st.checkbox("Show Raw Data"):
        st.write(data_cleaned)
