
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
    x_col = st.sidebar.selectbox("Select X-axis Column", data.columns)
    y_col = st.sidebar.selectbox("Select Y-axis Column", data.columns)
    plot_type = st.sidebar.radio("Select Plot Type", ["Line", "Bar", "Scatter"])

    # Clean data for the selected columns
    if data[x_col].isnull().sum() > 0 or data[y_col].isnull().sum() > 0:
        st.warning("Selected columns contain missing values. These rows will be dropped for visualization.")
        data_cleaned = data[[x_col, y_col]].dropna()
    else:
        data_cleaned = data[[x_col, y_col]]

    # Convert columns to numeric if possible
    try:
        data_cleaned[x_col] = pd.to_numeric(data_cleaned[x_col], errors='coerce')
        data_cleaned[y_col] = pd.to_numeric(data_cleaned[y_col], errors='coerce')
    except Exception as e:
        st.error(f"Error converting columns to numeric: {e}")
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
