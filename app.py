import os
from PIL import Image

import streamlit as st

from utils import (
    tesseract_ocr,
    abbyy_ocr,
)


st.title("Optical Character Recognition")
st.markdown("<br></br>", unsafe_allow_html=True)

# Main title
# st.sidebar.markdown(
#    "<center> <img src='picture.jpg' width='200'> </center>",
#    unsafe_allow_html=True,
# )
st.sidebar.image("picture.jpg", width=150, use_column_width=False)
st.sidebar.markdown("<br></br>", unsafe_allow_html=True)

# Settings

# OCR = st.multiselect(
#    "Select OCR engine",
#    ("Tesseract", "Abbyy")
# )
st.markdown("<b><h4>Select OCR engine</h4></b>", unsafe_allow_html=True)
OCR = st.selectbox(" ", ("Tesseract", "Abbyy"))
path = "data"

st.markdown("<b><h4>Upload a file to ocr</h4></b>", unsafe_allow_html=True)
uploaded_file = st.file_uploader(
    "", type=["jpg", "png", "jpeg"]
)

if uploaded_file is not None:
    # Use the file
    # st.markdown("**file to OCR**")
    uploaded_image = Image.open(uploaded_file)
    # Use the image
    # st.image(uploaded_image, width=1000, use_column_width=True)


if OCR == "Tesseract" and uploaded_file is not None:
    ocr_result = tesseract_ocr(uploaded_image, "eng")
    with open("ocr_result.txt", "w", encoding="utf-8") as file:
        file.write(ocr_result)
    st.download_button(
        label="Download OCR Result",
        data=open("ocr_result.txt", "r", encoding="utf-8").read(),
        file_name="ocr_result.txt",
        mime="text/plain",
    )


# Other info
st.sidebar.title("Description")
st.sidebar.info("This basic app can be used to ocr file with tesseracct and AbbyyOCR. ")
st.sidebar.title("Disclaimer")
st.sidebar.info(
    "For any questions or further details regarding techniques used, please contact egahepiphane@gmail.com"
)
