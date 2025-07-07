import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Page config
st.set_page_config(page_title="Network Intrusion Detection System", layout="wide")
st.title("🛡️ Network Intrusion Detection System (NIDS)")
st.markdown("Upload a preprocessed CSV file to detect intrusions using the trained model.")

# Upload CSV
uploaded_file = st.file_uploader(" Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)

        # Show preview
        st.subheader("Data Preview")
        st.write(data.head())

        # Clean negative values in numeric columns only
        numeric_cols = data.select_dtypes(include='number').columns
        data[numeric_cols] = data[numeric_cols].clip(lower=0)

        # Load the trained model and encoder
        model = joblib.load("model.pkl")
        encoder = joblib.load("encoder.pkl")

        # Label encoding if needed
        if 'Label' in data.columns:
            data['Label'] = encoder.transform(data['Label'])

        # Prediction (assumes features are all except 'Label')
        features = data.drop(columns=['Label']) if 'Label' in data.columns else data
        predictions = model.predict(features)

        # Add predictions to data
        data['Prediction'] = predictions

        # Map numeric prediction to labels (optional)
        data['Prediction_Label'] = data['Prediction'].map({0: 'Normal', 1: 'Attack'})

        # Show predictions
        st.subheader("🔎 Predictions")
        st.write(data[['Prediction', 'Prediction_Label']].value_counts())

        # Download result
        csv = data.to_csv(index=False).encode('utf-8')
        st.download_button(
            label=" Download Result CSV",
            data=csv,
            file_name='nids_predictions.csv',
            mime='text/csv'
        )

    except Exception as e:
        st.error(f" Error processing the file: {e}")

else:
    st.info("Upload a CSV file to begin analysis.")