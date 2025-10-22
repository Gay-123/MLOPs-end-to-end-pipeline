# streamlit_app.py
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
import pickle

# Load trained autoencoder
model = load_model("model/autoencoder_model.keras")

# Load training data used for threshold calculation
# This should be the same X_train you used to train the autoencoder
with open("model/X_train.pkl", "rb") as f:
    X_train = pickle.load(f)

# Automatically calculate threshold from training data
reconstruction_errors = np.mean(np.square(X_train - model.predict(X_train)), axis=1)
threshold = np.mean(reconstruction_errors) + 3 * np.std(reconstruction_errors)

st.title("Credit Card Fraud Detection")
st.write("Enter transaction details to detect potential fraud:")

# Collect inputs from user
amount = st.number_input("Transaction Amount", min_value=0.0, value=100.0)
time_since_last = st.number_input("Time Since Last Transaction (seconds)", min_value=0.0, value=3600.0)
spending_deviation = st.number_input("Spending Deviation Score", min_value=0.0, value=0.5)
velocity_score = st.number_input("Velocity Score", min_value=0.0, value=0.3)
geo_anomaly = st.number_input("Geo Anomaly Score", min_value=0.0, value=0.1)

# Prepare input array
X_input = np.array([[amount, time_since_last, spending_deviation, velocity_score, geo_anomaly]])

# Predict / reconstruct
reconstructed = model.predict(X_input)
reconstruction_error = np.mean(np.square(X_input - reconstructed))

st.write(f"Reconstruction Error: {reconstruction_error:.5f}")
st.write(f"Threshold (calculated from training data): {threshold:.5f}")

# Determine fraud or not
if reconstruction_error > threshold:
    st.error("⚠️ This transaction is likely FRAUDULENT!")
else:
    st.success("✅ This transaction looks NORMAL.")
