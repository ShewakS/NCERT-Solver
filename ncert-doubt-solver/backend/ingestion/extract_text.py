import fitz  # PyMuPDF
from pdfplumber import open as open_pdf
import pytesseract
from PIL import Image


def extract_text_from_pdf(path: str) -> list:
    """Return list of pages with text and metadata"""
    texts = []
    try:
        with open_pdf(path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text() or ""
                texts.append({"page": i, "text": text})
    except Exception:
        # Fallback using PyMuPDF + OCR
        doc = fitz.open(path)
        for i, page in enumerate(doc, start=1):
            pix = page.get_pixmap()
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            text = pytesseract.image_to_string(img, lang='eng')
            texts.append({"page": i, "text": text})
    return texts
