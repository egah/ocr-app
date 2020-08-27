from utils import tesseract_ocr, abbyy_ocr, cloudmersive_ocr , easy_ocr, asprise_ocr , bag_of_words, cosine_similarity
import streamlit as st
import pandas as pd
import time
import os, glob
from decimal import Decimal

st.title("Optical Character Recognition")
st.markdown("<br></br>",unsafe_allow_html=True)

# Main title
st.sidebar.markdown("<center> <img src='https://www.ccr-re.com/o/ccr-re-theme/images/footer-logos-groupe.png' width='200'> </center>",unsafe_allow_html=True)
st.sidebar.markdown("<br></br>",unsafe_allow_html=True)

# Settings
st.sidebar.title("Settings")

OCR = st.sidebar.multiselect('Select OCR engine',('Tesseract', 'Abbyy', 'EasyOCR', 'Cloudmersive OCR', 'Asprise OCR'))
path ='data'

filenames = [file for file in os.listdir(path) if  file[(len(file)-3):len(file)] in ['jpg','pdf','png']]
selected_filename = st.sidebar.selectbox('Select file to analyze', filenames)
file_jpg = os.path.join(path, selected_filename)
st.write('File `%s` has been selected' % file_jpg)
#image jpeg
st.markdown('**file to OCR**')
st.image(file_jpg, width=1000, use_column_width=True)
# document de reference
for file in glob.glob(os.path.join(path, '*.txt')):
    if selected_filename[0:-4]==file[5:-4]:
        with open(file, encoding='utf8',errors='ignore') as f:
            ref = f.read()
        break

# Other info
st.sidebar.title("Description")
st.sidebar.info("This basic app is at testing and comparing various OCR services applied to reinsurance documents")
st.sidebar.title("Disclaimer")
st.sidebar.info("For any questions or further details regarding techniques used, please contact acouloumy@ccr.fr")

# Calculations
df= pd.DataFrame(OCR)
Accuracy= []
cosine= []
temps= []
for elem in OCR:
    if elem == 'Tesseract':
        start= time.time()
        result= tesseract_ocr(file_jpg, 'eng+fra')
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        accuracy= bag_of_words(ref, result)
        temps.append(str(temp)+' s')
        Accuracy.append(str(accuracy)+' %')
        cosine.append(str(cosine_similarity(ref, result)))
        st.markdown('**Tesseract OCR Output**')
        st.text(result)
    elif elem== 'Abbyy':
        start= time.time()
        result= abbyy_ocr(file_jpg, "english,french")
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        accuracy= bag_of_words(ref, result)
        temps.append(str(temp)+' s')
        Accuracy.append(str(accuracy)+' %')
        cosine.append(str(cosine_similarity(ref, result)))
        st.markdown('** Abbyy OCR Output**')
        st.text(result)
    elif  elem=='EasyOCR':
        start= time.time()
        result= easy_ocr(file_jpg,0)
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        accuracy= bag_of_words(ref, result)
        temps.append(str(temp)+' s')
        Accuracy.append(str(accuracy)+' %')
        cosine.append(str(cosine_similarity(ref, result)))
        st.markdown('**EasyOCR Output**')
        st.text(result)
    elif elem=='Cloudmersive OCR':
        start= time.time()
        result= cloudmersive_ocr(file_jpg, 'ENG+FRA')
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        accuracy= bag_of_words(ref, result)
        temps.append(str(temp)+' s')
        Accuracy.append(str(accuracy)+' %')
        cosine.append(str(cosine_similarity(ref, result)))
        st.markdown('**Cloudmersive OCR Output**')
        st.text(result)
    elif elem== 'Asprise OCR':
        start= time.time()
        result= asprise_ocr(file_jpg, 'fra')
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        accuracy= bag_of_words(ref, result)
        temps.append(str(temp)+' s')
        Accuracy.append(str(accuracy)+' %')
        cosine.append(str(cosine_similarity(ref, result)))
        st.markdown('**Asprise OCR Output**')
        st.text(result)

st.markdown('**Metrics**')
df['time']=temps
df['word_accuracy']= Accuracy
df['cosine_similarity']= cosine
st.write(df.head())
