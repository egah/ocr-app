from cloudmersive_ocr_api_client.rest import ApiException
import easyocr
from scipy import spatial
import os
from ABBYY import CloudOCR
import cloudmersive_ocr_api_client
import numpy as np
import cv2
import pytesseract
from decimal import Decimal
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
from asprise_ocr_api import *

def tesseract_ocr(jpg_file, lang):
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
    configuration.api_key['Apikey'] = 'd572c584-3e08-460a-a999-498413d2c8ca'
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
