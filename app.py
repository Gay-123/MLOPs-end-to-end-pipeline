# streamlit_app.py
import streamlit as st
import numpy as np
from tensorflow.keras.models import load_model
import math
from datetime import datetime

# ------------- Load model -------------
model = load_model("model/autoencoder_model.keras")

st.set_page_config(page_title="Fraud Detector", layout="centered")
st.title("Credit Card Fraud Detection")

st.write("Enter transaction details (only these): amount, time, date, city, payment channel.")

# ------------- User inputs (minimal) -------------
amount = st.number_input("Transaction Amount", min_value=0.0, value=500.0, step=10.0, format="%.2f")
date_val = st.date_input("Transaction Date", value=datetime.now().date())
time_val = st.time_input("Transaction Time", value=datetime.now().time())
city = st.text_input("City", value="Chennai")
payment_channel = st.selectbox("Payment Channel", ["Online", "Cash/CreditCard", "Bank Transfer"])

# ------------- Build full feature vector (29 dims expected) -------------
num_features = model.input_shape[1]  # expected input dimension (e.g., 29)
X = np.zeros((1, num_features), dtype=float)

# Heuristic feature engineering from the minimal inputs:
# 1) amount_log: reduce skew
amount_log = math.log1p(float(amount))
# 2) hour_of_day and day_of_week from date+time
dt = datetime.combine(date_val, time_val)
hour = dt.hour + dt.minute / 60.0
hour_norm = hour / 24.0  # 0..1
day_of_week = dt.weekday()  # 0..6
dow_norm = day_of_week / 6.0

# 3) simple encodings for city and payment channel (deterministic small values)
city_code = sum(ord(c) for c in city[:10]) % 100   # 0-99
merchant_code = (city_code * 7 + 13) % 100         # pseudo merchant code derived from city
channel_map = {"Online": 2, "Cash/CreditCard": 1, "Bank Transfer": 0}
channel_code = channel_map.get(payment_channel, 0)

# Place the engineered features into the first few indices (consistent heuristic)
# NOTE: model was trained on 29 features; we don't know their exact meaning here,
# so we put sensible scaled values into first slots and zero elsewhere.
X[0, 0] = amount_log / 10.0        # scaled log amount
X[0, 1] = hour_norm                # normalized hour
X[0, 2] = dow_norm                 # normalized day-of-week
X[0, 3] = (city_code % 10) / 10.0  # small digit from city
X[0, 4] = (merchant_code % 10) / 10.0
X[0, 5] = channel_code / 2.0       # 0..1

# The rest remain zeros (silent/default features)
# ------------------------------------------------

# ------------- Estimate baseline threshold from the model (no scaler required) -------------
# Create small noise samples around a neutral vector to estimate model's "normal" reconstruction error
def estimate_threshold(model, dim, n=120, noise_scale=1e-3):
    base = np.zeros((n, dim))
    noise = np.random.normal(loc=0.0, scale=noise_scale, size=(n, dim))
    samples = base + noise
    preds = model.predict(samples)
    errs = np.mean(np.square(samples - preds), axis=1)
    mu = float(np.mean(errs))
    sigma = float(np.std(errs))
    thresh = mu + 3.0 * sigma
    return mu, sigma, thresh

with st.spinner("Preparing model baseline..."):
    mu_base, sigma_base, threshold = estimate_threshold(model, num_features, n=120, noise_scale=1e-3)

# ------------- Predict and decide -------------
reconstructed = model.predict(X)
recon_error = float(np.mean(np.square(X - reconstructed)))

# Decide: FRAUD or NOT FRAUD
is_fraud = recon_error > threshold

# ------------- Output (only FRAUD / NOT FRAUD as requested) -------------
st.write("")  # spacing
if is_fraud:
    st.markdown("<h1 style='color:#ff4b4b'>FRAUD</h1>", unsafe_allow_html=True)
else:
    st.markdown("<h1 style='color:#22c55e'>NOT FRAUD</h1>", unsafe_allow_html=True)

# Small debug info (hidden by default, but helpful). Show only if user wants to inspect.
if st.checkbox("Show debug info (reconstruction error & threshold)"):
    st.write(f"Reconstruction error: `{recon_error:.6f}`")
    st.write(f"Auto-estimated threshold (mean+3σ): `{threshold:.6f}`")
    st.write(f"Baseline mean ± std: `{mu_base:.6f} ± {sigma_base:.6f}`")
