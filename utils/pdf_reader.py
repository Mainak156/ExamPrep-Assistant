import pdfplumber
from pdf2image import convert_from_path
import pytesseract

def extract_text_from_pdf(pdf_path):
    extracted_text = ""

    with pdfplumber.open(pdf_path) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            text = page.extract_text()
            if text and text.strip():
                extracted_text += f"\n\n--- Page {page_num} ---\n{text}"
            else:
                image_text = extract_text_from_image_page(pdf_path, page_num)
                extracted_text += f"\n\n--- Page {page_num} (Image-based) ---\n{image_text}"

    return extracted_text

def extract_text_from_image_page(pdf_path, page_number):
    images = convert_from_path(pdf_path, first_page=page_number, last_page=page_number, dpi=300)
    page_text = ""

    for image in images:
        text = pytesseract.image_to_string(image)
        page_text += text.strip()

    return page_text
