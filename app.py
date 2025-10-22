# streamlit_credit_fraud.py
import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Load your trained autoencoder for fraud detection
model = load_model("model/autoencoder_model.keras")

st.title("Credit Card Fraud Detection using Autoencoder")
st.write("Upload your CSV file containing transaction data. The model will reconstruct normal transactions and flag anomalies based on reconstruction error.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV
    data = pd.read_csv(uploaded_file)
    st.write("Uploaded Data (first 5 rows):")
    st.dataframe(data.head())

    # Ensure only numeric features are used
    X = data.select_dtypes(include=[np.number]).values

    # Check feature count
    if X.shape[1] != model.input_shape[1]:
        st.error(f"Your data must have {model.input_shape[1]} features! Currently it has {X.shape[1]} features.")
    else:
        # Reconstruct data using autoencoder
        reconstructed = model.predict(X)

        # Calculate reconstruction error
        reconstruction_error = np.mean(np.square(X - reconstructed), axis=1)

        # Set threshold for anomaly (you can adjust based on training)
        threshold = np.percentile(reconstruction_error, 95)  # top 5% errors considered fraud
        is_fraud = reconstruction_error > threshold

        st.write("Reconstruction Error (first 10 rows):")
        st.dataframe(pd.DataFrame(reconstruction_error, columns=["Reconstruction Error"]).head(10))

        st.write("Fraud Detection (first 10 rows):")
        st.dataframe(pd.DataFrame(is_fraud, columns=["Is Fraud"]).head(10))

        st.line_chart(reconstruction_error)

        st.write(f"Threshold used for fraud detection: {threshold:.4f}")
        st.write(f"Number of transactions flagged as fraud: {np.sum(is_fraud)}")
