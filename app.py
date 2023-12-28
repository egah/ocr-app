from PIL import Image

import streamlit as st

from utils import tesseract_ocr


def main():
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

    st.markdown(
        "<b><h3 style='color: #3585CD;'>Select a language</h4></b>", unsafe_allow_html=True
    )
    language = None
    language = st.selectbox("", ["eng", "fra"])

    # TODO : add a possible languages support by tesseract
    # options = ['"france"', '"germany"', '"italy"', '"spain"', '"sweden"',]
    # Text input for filter criteria
    # filter = st.text_input('Enter filter criteria')
    # Filter options
    # filtered_options = [option for option in options if filter.lower() in option.lower()]
    # Select box with filtered options
    # selected_option = st.selectbox('', filtered_options)
    # st.write(f'You selected: {selected_option}')

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

    if language is not None and uploaded_file is not None:
        ocr_result = tesseract_ocr(uploaded_image, language)
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
    st.sidebar.info(
        "This basic app can be used to ocr (text to image) file with tesseract."
    )
    st.sidebar.title("Disclaimer")
    st.sidebar.info(
        "For any questions or further details regarding techniques used, please contact egahepiphane@gmail.com"
    )


if __name__ == "__main__":
    main()
