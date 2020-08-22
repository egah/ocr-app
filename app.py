import streamlit as st
import pandas as pd
import numpy as np
#import plotly.express as px
import glob
import numpy as np
import cv2
import pytesseract
from matplotlib import pyplot as plt
from pytesseract import Output
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
import tempfile
from PIL import Image
import os, subprocess
import time
from enum import Enum
from io import BytesIO, StringIO
from typing import Union
import ABBYY
import io
from ABBYY import CloudOCR
from enum import Enum
from io import BytesIO, StringIO
from typing import Union
import cloudmersive_ocr_api_client
#from __future__ import print_function
import time
from cloudmersive_ocr_api_client.rest import ApiException
from pprint import pprint
from asprise_ocr_api import *
import torch
import torchvision
import easyocr
from io import BufferedReader
import glob
from scipy import spatial
from decimal import Decimal
from bokeh.plotting import figure
st.title("Optical Character Recognition")


OCR= st.sidebar.selectbox('SELECT OCR ENGINE',('Tesseract', 'Abbyy', 'EasyOCR', 'Cloudmersive OCR', 'Asprise OCR'))
path=r'C:\Users\eepip\Desktop'

def file_selector(folder_path):
    filenames = [file for file in os.listdir(folder_path) if  file[(len(file)-3):len(file)] in ['jpg','pdf','png']]
    selected_filename = st.sidebar.selectbox('SELECT A FILE TO OCR', filenames)
    return os.path.join(folder_path, selected_filename)
file= file_selector(path)
st.write('You selected `%s`' % file)
def file_selector(folder_path):
    filenames= [file for file in os.listdir(folder_path) if  file[(len(file)-3):len(file)]=='txt']
    selected_filename = st.sidebar.selectbox('SELECT THE GROUND THRUTH FILE', filenames)
    return os.path.join(folder_path, selected_filename)
ref_file = file_selector(path)
st.write('You selected `%s`' % ref_file)
with open(ref_file, encoding='utf8',errors='ignore') as f:
    ref= f.read()

def tesseract_ocr(jpg_file, lang):
    #importaion de l'image
    image=cv2.imread(jpg_file)
    custom_config= r'--oem 1'
    text= pytesseract.image_to_string(image, lang=lang, config=custom_config)
    return text
def abbyy_ocr(jpg_file, lang):
    ocr_engine = CloudOCR(application_id='5766ee3d-45f0-4cf9-88c9-f51721847735', password='Su/SO91YzA2xjxCS30aAnL3P')
    jpg= open(jpg_file, 'rb')
    file = {jpg.name: jpg_file}
    result = ocr_engine.process_and_download(file, exportFormat='txt', language= lang)
    file = result.get('txt')
    return file.getvalue().decode("utf-8")
def easy_ocr(jpg_file, detail):
    lang1='en'
    lang2='fr'
    reader = easyocr.Reader([lang1, lang2],gpu = False)
    image= cv2.imread(jpg_file)
    text=reader.readtext(image, detail = detail ,paragraph = True)
    text= "\n".join(text)
    return text
def cloudmersive_ocr(jpg_file, lang):
    # Configure API key authorization: Apikey
    configuration = cloudmersive_ocr_api_client.Configuration()
    configuration.api_key['Apikey'] = '85d19384-bb8c-4388-a169-4b377558c881'
    # Uncomment below to setup prefix (e.g. Bearer) for API key, if needed
    # configuration.api_key_prefix['Apikey'] = 'Bearer'
    # create an instance of the API class
    api_instance = cloudmersive_ocr_api_client.ImageOcrApi(cloudmersive_ocr_api_client.ApiClient(configuration))
    image_file = jpg_file # file | Image file to perform OCR on.  Common file formats such as PNG, JPEG are supported.
    preprocessing = 'Auto'
    try:
        # Convert a scanned image into words with location
        api_response = api_instance.image_ocr_photo_to_text(image_file, language=lang)
        return api_response.text_result
    except ApiException as e:
        print("Exception when calling ImageOcrApi->image_ocr_image_lines_with_location: %s\n" % e)

def asprise_ocr(jpg_file, lang):
    Ocr.set_up() # one time setup
    ocrEngine = Ocr()
    ocrEngine.start_engine(lang)
    text = ocrEngine.recognize(jpg_file, -1, -1, -1, -1, -1, OCR_RECOGNIZE_TYPE_ALL, OCR_OUTPUT_FORMAT_PLAINTEXT)
    # recognizes more images here ..
    #ocrEngine.stop_engine()
    return text



def bag_of_words(verite_terrain, ocr_result):
    bag_ref= verite_terrain.split()
    bag_ocr= ocr_result.split()
    error= 0
    for elem in np.unique(bag_ref):
        error = error - bag_ocr.count(elem) + bag_ref.count(elem)
    acc= (len(bag_ref) - error)*100/len(bag_ref)
    acc_deci= Decimal(str(round(acc,2)))
    accuracy = float(acc_deci)
    return accuracy

def cosine_similarity(verite_terrain, ocr_result):
    bag_ref= verite_terrain.split()
    bag_ocr= ocr_result.split()
    ref_elem =[]
    doc_elem =[]
    for elem in np.unique(bag_ref):
        ref_elem.append(bag_ocr.count(elem))
        doc_elem.append(bag_ref.count(elem))
    result = 1 - spatial.distance.cosine(ref_elem, doc_elem)
    result_deci= Decimal(str(round(result,2)))
    cosine_sim=float(result_deci)
    return cosine_sim
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
