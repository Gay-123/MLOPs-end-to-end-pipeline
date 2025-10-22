# streamlit_app.py
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model

# --- Load your trained model ---
model = load_model("model/autoencoder_model.keras")

st.title("💳 Credit Card Fraud Detection")
st.write("Enter basic transaction details below and check if it might be fraudulent.")

# --- User Inputs (Human-friendly) ---
amount = st.number_input("Transaction Amount (₹)", min_value=0.0, value=500.0, step=10.0)
time_since_last = st.number_input("Time Since Last Transaction (in hours)", min_value=0.0, value=10.0, step=1.0)
location = st.text_input("Transaction Location", value="Chennai")
merchant_type = st.text_input("Merchant Type", value="Electronics")
payment_channel = st.selectbox("Payment Channel", ["Online", "POS", "ATM"])

# --- Build model input (dummy vector of 29 features) ---
num_features = model.input_shape[1]  # expected feature count (29)
X_input = np.zeros((1, num_features))

# Fill meaningful ones
X_input[0, 0] = amount
X_input[0, 1] = time_since_last

# Optionally encode location / merchant / payment as small numeric codes
# (for demonstration only, not from training)
X_input[0, 2] = len(location) % 10       # just a simple consistent encoding
X_input[0, 3] = len(merchant_type) % 10
X_input[0, 4] = 1 if payment_channel == "Online" else 0

# --- Prediction using autoencoder ---
reconstructed = model.predict(X_input)
reconstruction_error = np.mean(np.square(X_input - reconstructed))

st.write(f"🧮 Reconstruction Error: **{reconstruction_error:.6f}**")

# --- Decision threshold ---
threshold = 0.02  # adjust based on training
if reconstruction_error > threshold:
    st.error("⚠️ This transaction might be **FRAUDULENT!**")
else:
    st.success("✅ This transaction seems **Normal.**")

# --- Display entered data for clarity ---
st.subheader("Entered Transaction Details")
st.write({
    "Amount": amount,
    "Time Since Last Txn": time_since_last,
    "Location": location,
    "Merchant Type": merchant_type,
    "Payment Channel": payment_channel
})
