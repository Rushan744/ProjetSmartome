import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
uploaded_file = st.file_uploader("Upload your CSV file for visualization", type="csv")

if uploaded_file:
    try:
        # Read the dataset with semicolon as delimiter
        data = pd.read_csv(uploaded_file, delimiter=';', on_bad_lines='skip')
        st.success("Dataset loaded successfully!")
    except Exception as e:
        st.error(f"Error loading the dataset: {e}")
        st.stop()

    # Display the first few rows of the dataset
    st.write("### Dataset Preview")
    st.dataframe(data.head())

    # Visualization options
    st.sidebar.header("Visualization Options")
    x_col = st.sidebar.selectbox("Select X-axis Column", data.columns, key="x_col")
    y_col = st.sidebar.selectbox("Select Y-axis Column", data.columns, key="y_col")
    plot_type = st.sidebar.radio("Select Plot Type", ["Line", "Bar", "Scatter"], key="plot_type")

    # Clean data for the selected columns
    data_cleaned = data[[x_col, y_col]].dropna()

    try:
        # Check if selected columns exist
        if x_col not in data_cleaned.columns or y_col not in data_cleaned.columns:
            raise KeyError(f"Columns '{x_col}' or '{y_col}' are not found in the dataset.")

        # Check if columns contain valid data
        if data_cleaned[x_col].empty or data_cleaned[y_col].empty:
            raise ValueError(f"Columns '{x_col}' or '{y_col}' contain no data.")

        # Convert selected columns to numeric
        data_cleaned[x_col] = pd.to_numeric(data_cleaned[x_col], errors='coerce')
        data_cleaned[y_col] = pd.to_numeric(data_cleaned[y_col], errors='coerce')

        # Drop rows with NaN values after conversion
        data_cleaned = data_cleaned.dropna(subset=[x_col, y_col])

        # Check if the DataFrame is empty after cleaning
        if data_cleaned.empty:
            raise ValueError("The dataset is empty after cleaning. Ensure columns contain numeric data.")
    except KeyError as e:
        st.error(f"Column selection error: {e}")
        st.stop()
    except ValueError as e:
        st.error(f"Data validation error: {e}")
        st.stop()
    except Exception as e:
        st.error(f"Unexpected error while converting columns to numeric: {e}")
        st.stop()

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
        st.write(data)

 