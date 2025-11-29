import streamlit as st
import pandas as pd
import numpy as np
from streamlit_image_zoom import image_zoom
from PIL import Image

st.title("Record Linkage GUI")
st.sidebar.header("Controls")

if "zoom" not in st.session_state: 
    st.session_state.zoom = 1.0



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



def upload_image_files():
    image_files = st.file_uploader("Upload images", accept_multiple_files=True, type=["jpg","jpeg","png"])
    if image_files:
        for image_file in image_files:
            image = Image.open(image_file)
            image_width, image_height = image.size

            image_zoom(image, mode="scroll", size=(int(image_width/2), int(image_height/2)), keep_aspect_ratio=False, zoom_factor=4.0, increment=0.2)

upload_image_files()
