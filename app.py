import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load the saved model and encoder
model = joblib.load("random_forest_nids_model.pkl")
encoder = joblib.load("label_encoder.pkl")

# Streamlit app title
st.title("Network Intrusion Detection System (NIDS)")

# Upload CSV file
uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data", data.head())

    # Clean data
    data = data.fillna(0)
    data[data < 0] = 0

    # Predict
    predictions = model.predict(data)
    predicted_labels = encoder.inverse_transform(predictions)

    # Add predictions to dataframe
    data["Predicted Attack Type"] = predicted_labels
    st.write("Prediction Results", data[["Predicted Attack Type"]])

    # Download button
    csv = data.to_csv(index=False)
    st.download_button("Download Predictions", csv, "predictions.csv", "text/csv")
