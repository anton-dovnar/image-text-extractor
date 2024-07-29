import pytesseract
from PIL import Image
from pdf2image import convert_from_path

from django.conf import settings


def check_file(file_name):
    # Define file formats and their handlers
    image_formats = {'jpg', 'png', 'jpeg'}
    handlers = {
        'jpg': extract_text_from_image,
        'png': extract_text_from_image,
        'jpeg': extract_text_from_image,
        'pdf': extract_text_from_pdf,
    }
    
    # Extract file format
    format = file_name.rsplit('.', 1)[-1].lower()
    
    # Get file path
    file_path = settings.BASE_DIR / 'myapp/static/media' / file_name
    
    # Check if the format is supported
    if format not in handlers:
        raise ValueError(f"Unsupported file format: {format}")

    # Process file based on its format
    if format in image_formats:
        try:
            image = Image.open(file_path)
            return handlers[format](image)
        except Exception as e:
            raise RuntimeError(f"Error processing image file: {e}")
    else:
        try:
            return handlers[format](file_path)
        except Exception as e:
            raise RuntimeError(f"Error processing PDF file: {e}")


def extract_text_from_image(image):
    extracted_text = pytesseract.image_to_string(image, lang='eng')
    return extracted_text


def extract_text_from_pdf(pdf):
    pages = convert_from_path(pdf,last_page=5)
    text =''
    for page in pages:
        text += str(extract_text_from_image(page))

    return text


def handle_uploaded_file(f):  
    file_name = f.name
    with open('myapp/static/media/'+file_name, 'wb+') as destination:  
        for chunk in f.chunks():  
            destination.write(chunk)
    return file_name