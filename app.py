# app.py

import streamlit as st
import pandas as pd
import joblib
from sklearn.preprocessing import LabelEncoder


@st.cache_resource
def load_model():
    model = joblib.load("random_forest_nids_model.pkl")
    encoder = joblib.load("label_encoder.pkl")
    return model, encoder

model, label_encoder = load_model()

st.set_page_config(page_title="Network Intrusion Detection System", layout="wide")

st.title("📡 Network Intrusion Detection System (NIDS)")
st.write("Upload a cleaned CSV file to classify network traffic as Normal or Attack.")

# -----------------------
# File upload
# -----------------------
uploaded_file = st.file_uploader(" Upload a CSV file", type=["csv"])

if uploaded_file:
    try:
        # Read CSV
        df = pd.read_csv(uploaded_file)

        # Clean negative values
        df[df < 0] = 0

        # Predict
        predictions = model.predict(df)
        decoded_preds = label_encoder.inverse_transform(predictions)

        # Display predictions
        st.subheader("Prediction Results")
        st.write(f"Total records: {len(df)}")
        st.write(f" Attack types detected: {set(decoded_preds)}")
        st.dataframe(pd.DataFrame({"Prediction": decoded_preds}))

        # Download results
        output_df = df.copy()
        output_df["Prediction"] = decoded_preds
        csv = output_df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇️ Download Prediction CSV", csv, "nids_predictions.csv", "text/csv")

    except Exception as e:
        st.error(f"Error processing the file: {e}")

else:
    st.info("Upload a CSV file to begin.")
