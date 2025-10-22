# streamlit_app.py
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model

# Load the trained autoencoder model
model = load_model("model/autoencoder_model.keras")

st.title("Credit Card Fraud Detection")
st.write("Enter the transaction details below and detect potential fraud.")

# Human-friendly transaction inputs
amount = st.number_input("Transaction Amount", min_value=0.0, value=100.0)
time_since_last = st.number_input("Time Since Last Transaction (hours)", min_value=0.0, value=24.0)

# Optional info for location and merchant type (not used by model here, just for display)
location = st.text_input("Transaction Location", value="CityX")
merchant_type = st.text_input("Merchant Type", value="Retail")

# --- Feature engineering for model input ---
# These are derived features your autoencoder expects
# In a real scenario, these would be computed from user history
spending_deviation_score = 0.5  # default placeholder
velocity_score = 0.3            # default placeholder
geo_anomaly_score = 0.2         # default placeholder

# Combine into array for model
X_input = np.array([[amount, time_since_last, spending_deviation_score,
                     velocity_score, geo_anomaly_score]])

# Predict reconstruction
reconstructed = model.predict(X_input)
reconstruction_error = np.mean(np.square(X_input - reconstructed))

st.write(f"Reconstruction Error: {reconstruction_error:.4f}")

# Decide fraud or not
threshold = 0.02  # tune this based on training data
if reconstruction_error > threshold:
    st.error("⚠️ This transaction might be FRAUDULENT!")
else:
    st.success("✅ This transaction seems normal.")
