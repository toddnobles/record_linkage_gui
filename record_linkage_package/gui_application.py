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
else:
    st.warning("Please upload a csv file.")


def upload_image_folder():
    image_folder = st.file_uploader("Upload folder of images", accept_multiple_files=True, type=["jpg","jpeg","png"])
    if image_folder:
        for image_file in image_folder:
            st.image(image_file)

upload_image_folder()