import streamlit as st
import pandas as pd
import joblib

# Load model and scaler from the model folder
model = joblib.load("model/fraud_model.pkl")
scaler = joblib.load("model/scaler.pkl")

# Streamlit page setup
st.set_page_config(page_title="Real-Time Fraud Detection", layout="centered")
st.title("🔍 Real-Time Fraud Detection")
st.write("Enter transaction details below to assess fraud risk:")

# Transaction input form
with st.form("transaction_form"):
    amount = st.number_input("Transaction Amount", min_value=0.0)
    transaction_type = st.selectbox("Transaction Type", ["debit", "credit"])
    weekday = st.selectbox("Weekday", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
    hour = st.slider("Hour", 0, 23)
    minute = st.slider("Minute", 0, 59)
    second = st.slider("Second", 0, 59)
    time_since_last_transaction = st.number_input("Time Since Last Transaction (seconds)", min_value=0.0)
    spending_deviation_score = st.slider("Spending Deviation Score", 0.0, 1.0, 0.5)
    velocity_score = st.slider("Velocity Score", 0.0, 1.0, 0.5)
    geo_anomaly_score = st.slider("Geo Anomaly Score", 0.0, 1.0, 0.5)

    submitted = st.form_submit_button("Predict Fraud Risk")

# Map weekday to numeric
weekday_map = {"Monday":0, "Tuesday":1, "Wednesday":2, "Thursday":3, "Friday":4, "Saturday":5, "Sunday":6}
weekday_val = weekday_map[weekday]

# Predict if form is submitted
if submitted:
    input_data = pd.DataFrame([{
        "amount": amount,
        "hour": hour,
        "minute": minute,
        "second": second,
        "weekday": weekday_val,
        "time_since_last_transaction": time_since_last_transaction,
        "spending_deviation_score": spending_deviation_score,
        "velocity_score": velocity_score,
        "geo_anomaly_score": geo_anomaly_score,
        "transaction_type_credit": 1 if transaction_type == "credit" else 0  # one-hot encoded
    }])

    # Scale input
    input_scaled = scaler.transform(input_data)

    # Predict
    prob = model.predict_proba(input_scaled)[0][1]
    label = "⚠️ FRAUD" if prob > 0.5 else "✅ Legit"

    st.metric(label="Fraud Risk Score", value=f"{prob:.3f}")
    st.success(label)
