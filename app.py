import os
from PIL import Image

import streamlit as st

from utils import (
    tesseract_ocr,
    abbyy_ocr,
)

st.set_page_config(
    page_title="OCR Engine",
    layout="centered",
    initial_sidebar_state="expanded",
    page_icon=":mag:",
)

st.title("Optical Character Recognition")

# Main title
# st.sidebar.markdown(
#    "<center> <img src='picture.jpg' width='200'> </center>",
#    unsafe_allow_html=True,
# )

st.sidebar.image("picture.jpg", width=200, use_column_width=False)

# with open("description.html", mode="r") as description:
#    html_file = description.read()
# st.sidebar.markdown(html_file, unsafe_allow_html=True)
st.sidebar.caption("# Epiphane Egah 🤗️🚀️\n")
st.sidebar.info(
    """Analytics Enginee : Python - NLP - Statistics - Machine learning -
    Deep learning  - DevOps - MLops"""
)

# Settings

# OCR = st.multiselect(
#    "Select OCR engine",
#    ("Tesseract", "Abbyy")
# )
st.markdown(
    "<b><h3 style='color: #77B5FE;'>Select OCR engine</h4></b>", unsafe_allow_html=True
)
OCR = st.selectbox(" ", ("Tesseract", "Abbyy"))
path = "data"

st.markdown(
    "<b><h3 style='color: #FF0000;'>Upload a file</h4></b>", unsafe_allow_html=True
)
uploaded_file = st.file_uploader("", type=["jpg", "png", "jpeg"])

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
