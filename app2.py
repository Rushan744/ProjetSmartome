import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Title
st.title("Data Visualisation")

# Upload multiple CSV files
uploaded_files = st.file_uploader(
    "Upload your CSV files (up to 5)", 
    type="csv", 
    accept_multiple_files=True
)

# Store uploaded datasets
datasets = {}

if uploaded_files:
    for i, file in enumerate(uploaded_files):
        try:
            # Read each dataset
            data = pd.read_csv(file, delimiter=';', on_bad_lines='skip')
            datasets[f"Dataset {i+1}"] = data
            st.success(f"Successfully loaded Dataset {i+1}")
        except Exception as e:
            st.error(f"Error loading Dataset {i+1}: {e}")

    # Dropdown to select a dataset
    dataset_name = st.selectbox("Select a Dataset for Visualization", options=list(datasets.keys()))

    if dataset_name:
        # Get selected dataset
        selected_data = datasets[dataset_name]

        # Display the first few rows
        st.write(f"### {dataset_name} Preview")
        st.dataframe(selected_data.head())

        # Visualization options
        st.sidebar.header(f"Visualization Options for {dataset_name}")
        x_col = st.sidebar.selectbox("Select X-axis Column", selected_data.columns, key=f"{dataset_name}_x")
        y_col = st.sidebar.selectbox("Select Y-axis Column", selected_data.columns, key=f"{dataset_name}_y")
        plot_type = st.sidebar.radio("Select Plot Type", ["Line", "Bar", "Scatter"], key=f"{dataset_name}_plot")

        # Clean data for the selected columns
        data_cleaned = selected_data[[x_col, y_col]].dropna()

        try:
            # Convert columns to numeric
            data_cleaned[x_col] = pd.to_numeric(data_cleaned[x_col], errors='coerce')
            data_cleaned[y_col] = pd.to_numeric(data_cleaned[y_col], errors='coerce')

            # Drop rows with NaN values after conversion
            data_cleaned = data_cleaned.dropna(subset=[x_col, y_col])

            if data_cleaned.empty:
                raise ValueError("Data is empty after cleaning. Check your dataset for valid numeric values.")

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
                st.write(selected_data)
        except ValueError as e:
            st.error(f"Value Error: {e}")
        except Exception as e:
            st.error(f"Unexpected error: {e}")
