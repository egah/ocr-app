from utils import tesseract_ocr, abbyy_ocr, cloudmersive_ocr , easy_ocr, asprise_ocr , bag_of_words, cosine_similarity
import streamlit as st
import pandas as pd
import time
import os
from decimal import Decimal


st.title("Optical Character Recognition")
st.markdown("<br></br>",unsafe_allow_html=True)

# Main title
st.sidebar.markdown("<center> <img src='https://www.ccr-re.com/o/ccr-re-theme/images/footer-logos-groupe.png' width='200'> </center>",unsafe_allow_html=True)
st.sidebar.markdown("<br></br>",unsafe_allow_html=True)

# Settings
st.sidebar.title("Settings")

OCR = st.sidebar.selectbox('Select OCR engine',('Tesseract', 'Abbyy', 'EasyOCR', 'Cloudmersive OCR', 'Asprise OCR'))
path ='data'

filenames = [file for file in os.listdir(path) if  file[(len(file)-3):len(file)] in ['jpg','pdf','png']]
selected_filename = st.sidebar.selectbox('Select file to analyze', filenames)
file = os.path.join(path, selected_filename)
st.write('File `%s` has been selected' % file)

filenames= [file for file in os.listdir(path) if file[(len(file)-3):len(file)]=='txt']
selected_filename = st.sidebar.selectbox('Select file for control', filenames)
ref_file = os.path.join(path, selected_filename)
with open(ref_file, encoding='utf8',errors='ignore') as f:
    ref = f.read()

# Other info
st.sidebar.title("Description")
st.sidebar.info("This basic app is at testing and comparing various OCR services applied to reinsurance documents")
st.sidebar.title("Disclaimer")
st.sidebar.info("For any questions or further details regarding techniques used, please contact acouloumy@ccr.fr")

# Calculations

if file[23:-4]==ref_file[23:-4]:
    if OCR == 'Tesseract':
        start= time.time()
        result= tesseract_ocr(file, 'eng+fra')
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        st.markdown('**OCR Output**')
        st.text(result)
        accuracy= bag_of_words(ref, result)
        df_1= pd.DataFrame(index= ['Teseract'])
        df_1['Accuracy']= str(accuracy)+' %'
        df_1['time']= str(temp)+' s'
        df_1['cosine_similarity']= str(cosine_similarity(ref, result))
        st.markdown('**Metrics :**')
        st.write(df_1.head())
    elif OCR== 'Abbyy':
        start= time.time()
        result= abbyy_ocr(file, "english,french")
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        st.markdown('**OCR Output**')
        st.text(result)
        accuracy= bag_of_words(ref, result)
        df_1= pd.DataFrame(index= ['Abbyy'])
        df_1['Accuracy']= str(accuracy)+' %'
        df_1['time']= str(temp)+' s'
        df_1['cosine_similarity']= str(cosine_similarity(ref, result))
        st.markdown('**Metrics :**')
        st.write(df_1.head())
    elif  OCR=='EasyOCR':
        start= time.time()
        result= easy_ocr(file,0)
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        st.markdown('**OCR Output**')
        st.text(result)
        accuracy= bag_of_words(ref, result)
        df_1= pd.DataFrame(index= ['EasyOCR'])
        df_1['Accuracy']= str(accuracy)+' %'
        df_1['time']= str(temp)+' s'
        df_1['cosine_similarity']= str(cosine_similarity(ref, result))
        st.markdown('**Metrics :**')
        st.write(df_1.head())
    elif OCR=='Cloudmersive OCR':
        start= time.time()
        result= cloudmersive_ocr(file, 'ENG+FRA')
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        st.markdown('**OCR Output**')
        st.text(result)
        accuracy= bag_of_words(ref, result)
        df_1= pd.DataFrame(index= ['Cloudmersive OCR'])
        df_1['Accuracy']= str(accuracy)+' %'
        df_1['time']= str(temp)+' s'
        df_1['cosine_similarity']= str(cosine_similarity(ref, result))
        st.markdown('**Metrics :**')
        st.write(df_1.head())
    elif OCR== 'Asprise OCR':
        start= time.time()
        result= asprise_ocr(file, 'fra')
        end= time.time()
        temp=float(Decimal(str(round(end - start,2))))
        st.markdown('**OCR Output**')
        st.text(result)
        accuracy= bag_of_words(ref, result)
        df_1= pd.DataFrame(index= ['Asprise OCR'])
        df_1['Accuracy']= str(accuracy)+' %'
        df_1['time']= str(temp)+' s'
        df_1['cosine_similarity']= str(cosine_similarity(ref, result))
        st.markdown('**Metrics :**')
        st.write(df_1.head())


else: st.write("le document de référence et le document à océriser ne correspondent pas")
