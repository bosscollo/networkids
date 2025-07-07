# app.py

import streamlit as st
import pandas as pd
import joblib

# --- Load Model and Encoder ---
model = joblib.load("nids_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")

# --- Load Expected Features (from training) ---
expected_features = list(model.feature_names_in_)

st.set_page_config(page_title="NIDS Predictor", layout="wide")
st.title("Network Intrusion Detection System (NIDS)")
st.markdown("Upload your network CSV sample (even with partial features) to predict potential threats.")

# --- Upload Section ---
uploaded_file = st.file_uploader("📄 Upload CSV File", type=["csv"])

if uploaded_file:
    try:
        # Load CSV
        df = pd.read_csv(uploaded_file)

        # Identify missing and extra columns
        missing = [col for col in expected_features if col not in df.columns]
        extra = [col for col in df.columns if col not in expected_features]

        # Drop unknown columns
        df = df.drop(columns=extra, errors='ignore')

        # Fill missing columns with 0
        for col in missing:
            df[col] = 0

        # Reorder columns to match model input
        df = df[expected_features]

        # Prediction
        predictions = model.predict(df)
        decoded_preds = label_encoder.inverse_transform(predictions)

        df['Prediction'] = decoded_preds
        st.success("✅ Prediction completed.")
        st.dataframe(df[['Prediction']])

        # Download results
        st.download_button(
            label="📥 Download Results as CSV",
            data=df.to_csv(index=False),
            file_name="nids_predictions.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"⚠️ Error processing file: {e}")

else:
    st.info("Upload a CSV file to begin.")