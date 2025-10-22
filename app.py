# streamlit_app.py
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
import math
from datetime import datetime

# Load the trained model
model = load_model("model/autoencoder_model.keras")

st.set_page_config(page_title="Fraud Detector", layout="centered")
st.title("💳 Credit Card Fraud Detection")

st.write("Enter transaction details and click **Check Transaction** to predict fraud status.")

# -------- User inputs --------
amount = st.number_input("Transaction Amount", min_value=0.0, value=500.0, step=10.0, format="%.2f")
date_val = st.date_input("Transaction Date", value=datetime.now().date())
time_val = st.time_input("Transaction Time", value=datetime.now().time())
city = st.text_input("City", value="Chennai")
payment_channel = st.selectbox("Payment Channel", ["Online", "Cash/CreditCard", "Bank Transfer"])

# -------- Build full feature vector (29 features expected) --------
num_features = model.input_shape[1]
X = np.zeros((1, num_features), dtype=float)

# Heuristic feature setup
amount_log = math.log1p(float(amount))
dt = datetime.combine(date_val, time_val)
hour = dt.hour + dt.minute / 60.0
hour_norm = hour / 24.0
day_of_week = dt.weekday()
dow_norm = day_of_week / 6.0
city_code = sum(ord(c) for c in city[:10]) % 100
merchant_code = (city_code * 7 + 13) % 100
channel_map = {"Online": 2, "Cash/CreditCard": 1, "Bank Transfer": 0}
channel_code = channel_map.get(payment_channel, 0)

X[0, 0] = amount_log / 10.0
X[0, 1] = hour_norm
X[0, 2] = dow_norm
X[0, 3] = (city_code % 10) / 10.0
X[0, 4] = (merchant_code % 10) / 10.0
X[0, 5] = channel_code / 2.0

# -------- Estimate threshold once --------
@st.cache_resource
@st.cache_resource
def estimate_threshold(model, dim, n=120, noise_scale=1e-3):
    base = np.zeros((n, dim))
    noise = np.random.normal(loc=0.0, scale=noise_scale, size=(n, dim))
    samples = base + noise
    preds = model.predict(samples)
    errs = np.mean(np.square(samples - preds), axis=1)
    mu = float(np.mean(errs))
    sigma = float(np.std(errs))
    return mu, sigma, mu + 3.0 * sigma

mu_base, sigma_base, threshold = estimate_threshold(model, num_features)


# -------- Predict only when button clicked --------
if st.button("Check Transaction"):
    reconstructed = model.predict(X)
    recon_error = float(np.mean(np.square(X - reconstructed)))
    is_fraud = recon_error > threshold

    if is_fraud:
        st.markdown("<h2 style='color:#ff4b4b'>🚨 FRAUD DETECTED!</h2>", unsafe_allow_html=True)
    else:
        st.markdown("<h2 style='color:#22c55e'>✅ Not Fraudulent</h2>", unsafe_allow_html=True)

    with st.expander("Show Details"):
        st.write(f"Reconstruction Error: `{recon_error:.6f}`")
        st.write(f"Auto Threshold: `{threshold:.6f}`")
        st.json({
            "Amount": amount,
            "Date": str(date_val),
            "Time": str(time_val),
            "City": city,
            "Payment Channel": payment_channel
        })
else:
    st.info("➡️ Fill the details and click **Check Transaction** to get prediction.")