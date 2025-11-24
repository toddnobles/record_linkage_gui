import streamlit as st
import pandas as pd
import numpy as np

st.title("Record Linkage GUI")

def load_csv():
    uploaded_csv = st.file_uploader('Upload a CSV', type="csv", accept_multiple_files=False)
    if uploaded_csv:
        return pd.read_csv(uploaded_csv)
    else:
        return None
    
df = load_csv()
if df is not None:
    st.write(df)