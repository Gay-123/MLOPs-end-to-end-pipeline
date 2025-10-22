# streamlit_app.py
import streamlit as st
import pandas as pd
import numpy as np
from tensorflow.keras.models import load_model

# Load your trained autoencoder
model = load_model("autoencoder_model.keras")

st.title("Autoencoder Demo")
st.write("Upload your CSV data to see the autoencoder reconstruction results.")

# File uploader
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

if uploaded_file is not None:
    # Read CSV
    data = pd.read_csv(uploaded_file)
    st.write("Original Data:")
    st.dataframe(data.head())

    # Make sure the data is numeric
    X = data.select_dtypes(include=[np.number]).values

    if X.shape[1] != model.input_shape[1]:
        st.error(f"Your data must have {model.input_shape[1]} features!")
    else:
        # Predict / reconstruct
        reconstructed = model.predict(X)
        reconstruction_error = np.mean(np.square(X - reconstructed), axis=1)

        st.write("Reconstructed Data (first 5 rows):")
        st.dataframe(pd.DataFrame(reconstructed, columns=data.columns).head())

        st.write("Reconstruction Error (first 10 rows):")
        st.dataframe(pd.DataFrame(reconstruction_error, columns=["Reconstruction Error"]).head(10))

        st.line_chart(reconstruction_error)