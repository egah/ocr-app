from scipy import spatial
from ABBYY import CloudOCR
import numpy as np
import cv2
import pytesseract
from decimal import Decimal

pytesseract.pytesseract.tesseract_cmd = "tesseract"


def tesseract_ocr(image_to_ocr, lang):
    custom_config = r"--oem 1"
    text = pytesseract.image_to_string(image_to_ocr, lang=lang, config=custom_config)
    return text


def abbyy_ocr(jpg_file, lang):
    ocr_engine = CloudOCR(
        application_id="5766ee3d-45f0-4cf9-88c9-f51721847735",
        password="Su/SO91YzA2xjxCS30aAnL3P",
    )
    jpg = open(jpg_file, "rb")
    file = {jpg.name: jpg_file}
    result = ocr_engine.process_and_download(file, exportFormat="txt", language=lang)
    file = result.get("txt")
    return file.getvalue().decode("utf-8")


def bag_of_words(verite_terrain, ocr_result):
    bag_ref = verite_terrain.split()
    bag_ocr = ocr_result.split()
    error = 0
    for elem in np.unique(bag_ref):
        error = error - bag_ocr.count(elem) + bag_ref.count(elem)
    acc = (len(bag_ref) - error) * 100 / len(bag_ref)
    acc_deci = Decimal(str(round(acc, 2)))
    accuracy = float(acc_deci)
    return accuracy


def cosine_similarity(verite_terrain, ocr_result):
    bag_ref = verite_terrain.split()
    bag_ocr = ocr_result.split()
    ref_elem = []
    doc_elem = []
    for elem in np.unique(bag_ref):
        ref_elem.append(bag_ocr.count(elem))
        doc_elem.append(bag_ref.count(elem))
    result = 1 - spatial.distance.cosine(ref_elem, doc_elem)
    result_deci = Decimal(str(round(result, 2)))
    cosine_sim = float(result_deci)
    return cosine_sim


if __name__ == "__main__":
    pass
