# Network Intrusion Detection System (Networkids) Using Machine Learning -
'Ps nothing to do with kids it's IDS'

This project is part of the AI Mini-Project. It demonstrates how machine learning can be applied to detect malicious network traffic in real-time. The goal is to build a system that can classify network connections as either normal or as different types of attacks, such as DDoS, Brute Force, or Port Scanning.

###  Problem Statement
Networks today are constantly exposed to cyber threats. Detecting these threats early can help organizations prevent data loss, downtime, and financial loss. Our aim is to build an intelligent Network Intrusion Detection System that can learn from existing data and classify new traffic accurately.

### Dataset
- **Name:** CICIDS2017 (Cleaned and Preprocessed Version)
- **Source:** [Kaggle Dataset](https://www.kaggle.com/ericanacletoribeiro/cicids2017-cleaned-and-preprocessed)
- **Description:** The dataset contains 52 features and a labeled attack column with types such as DDoS, Brute Force, Web Attacks, etc.

### Technologies Used
- Python (Pandas, NumPy, Scikit-learn, Joblib)
- Streamlit for Web Deployment
- Google Colab for Development
- Label Encoding and Random Forest for modeling

### How It Works
1. The data was cleaned and preprocessed (null values, label encoding, outliers handled)
2. Trained a **Random Forest Classifier** using supervised learning
3. The model was evaluated and achieved high accuracy
4. The final model was deployed as a **Streamlit Web App**

### Live Demo
Upload a CSV of network traffic and get predictions:
 [Try the App](https://networkids.streamlit.app)

###  Files Included
- `df_cleaned.csv`: Preprocessed dataset
- `random_forest_nids_model.pkl`: Trained ML model
- `label_encoder.pkl`: Label encoder for attack labels
- `app.py`: Streamlit interface
