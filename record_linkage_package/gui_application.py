import streamlit as st
import pandas as pd
import numpy as np

st.title("Record Linkage GUI")

uploaded_files = st.file_uploader('Upload a CSV', type="csv", accept_multiple_files=True)

def load_csv():
    if uploaded_files:
        for uploaded_file in uploaded_files:
            df = pd.read_csv(uploaded_file)
            st.write(df.head())