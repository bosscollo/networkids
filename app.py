import streamlit as st
import pandas as pd
import numpy as np
import joblib

# Load model & label encoder
@st.cache_resource
def load_model():
    model = joblib.load("nids_model.pkl")
    encoder = joblib.load("label_encoder.pkl")
    return model, encoder

model, label_encoder = load_model()

# Page setup
st.set_page_config(page_title="Network IDS", layout="wide")
st.title("📡 Network Intrusion Detection System (ML-Powered)")

# Upload
uploaded_file = st.file_uploader("📁 Upload a preprocessed CSV file", type=["csv"])

if uploaded_file:
    try:
        # Load and preview
        df = pd.read_csv(uploaded_file)
        st.subheader("📊 Uploaded Preview")
        st.dataframe(df.head())

        # Drop any non-feature columns just in case
        to_drop = ['Attack Type', 'Attack type', 'Label', 'Protocol']
        df = df.drop(columns=[col for col in to_drop if col in df.columns], errors='ignore')

        # Only use numeric features (as model was trained on 53 normalized columns)
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        df[numeric_cols] = df[numeric_cols].apply(
            lambda x: (x - x.min()) / (x.max() - x.min())
        )

        # Ensure column match
        expected_cols = model.feature_names_in_
        df = df[[col for col in expected_cols if col in df.columns]]

        # Prediction
        preds = model.predict(df)
        labels = label_encoder.inverse_transform(preds)

        st.subheader("✅ Prediction Results")
        st.dataframe(pd.DataFrame({"Prediction": labels}))

        # Download results
        df_out = df.copy()
        df_out["Prediction"] = labels
        st.download_button("⬇️ Download CSV", df_out.to_csv(index=False), "nids_predictions.csv", "text/csv")

    except Exception as e:
        st.error(f"Error processing the file: {e}")
else:
    st.info("Upload a CSV file above to begin prediction.")