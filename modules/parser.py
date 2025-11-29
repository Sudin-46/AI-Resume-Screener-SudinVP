import io
from PyPDF2 import PdfReader

def extract_text_from_pdf(uploaded_file):
    # Read file data
    data = uploaded_file.read()

    # Initialize PDF reader
    reader = PdfReader(io.BytesIO(data))

    text = []
    for page in reader.pages:
        page_text = page.extract_text() or ''
        text.append(page_text)

    return "\n".join(text)
