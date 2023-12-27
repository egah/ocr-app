import pytesseract

pytesseract.pytesseract.tesseract_cmd = "tesseract"


def tesseract_ocr(image_to_ocr, lang):
    custom_config = r"--oem 1"
    text = pytesseract.image_to_string(image_to_ocr, lang=lang, config=custom_config)
    return text
