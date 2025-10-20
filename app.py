import streamlit as st
import joblib
import pandas as pd

# Load model and encoders
model = joblib.load("model/svm_best_model_1.pkl")
le_loyalty = joblib.load("model/le_loyalty.pkl")
le_location = joblib.load("model/le_location.pkl")
le_payment = joblib.load("model/le_payment.pkl")
le_device = joblib.load("model/le_device.pkl")

st.title("💳 Credit Card Fraud Detection App")
st.write("Enter transaction details below to check if it's Fraudulent or Not 👇")

# Input fields
customer_age = st.number_input("Customer Age", min_value=18, max_value=100, value=30)
loyalty_tier = st.selectbox("Customer Loyalty Tier", ["Bronze", "Silver", "Gold", "Platinum"])
location = st.selectbox("Location", ["New York", "San Francisco", "Chicago", "Los Angeles"])
purchase_amount = st.number_input("Purchase Amount ($)", min_value=1.0, value=150.0)
payment_method = st.selectbox("Payment Method", ["Credit Card", "Debit Card", "Mobile Payment", "Cash"])
device_type = st.selectbox("Device Type", ["Mobile", "Desktop", "Tablet"])
footfall_count = st.number_input("Footfall Count", min_value=0, value=200)
transaction_hour = st.slider("Transaction Hour (24-hour format)", 0, 23, 14)

if st.button("Predict Fraud"):
    # Encode categorical features
    loyalty_enc = le_loyalty.transform([loyalty_tier])[0]
    location_enc = le_location.transform([location])[0]
    payment_enc = le_payment.transform([payment_method])[0]
    device_enc = le_device.transform([device_type])[0]

    # Prepare data
    input_data = pd.DataFrame({
        "Customer_Age": [customer_age],
        "Customer_Loyalty_Tier": [loyalty_enc],
        "Location": [location_enc],
        "Purchase_Amount": [purchase_amount],
        "Payment_Method": [payment_enc],
        "Device_Type": [device_enc],
        "Footfall_Count": [footfall_count],
        "Transaction_Hour": [transaction_hour]
    })

    # Predict
    prediction = model.predict(input_data)[0]

    if prediction == 1:
        st.error("🚨 Transaction is FRAUDULENT!")
    else:
        st.success("✅ Transaction is LEGITIMATE.")
