from flask import Flask,render_template, request
from PIL import Image
from pdf2image import convert_from_bytes
import pytesseract
import os
app = Flask(__name__)

ALLOWED_EXTENSIONS = ['.pdf','.png']

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_file', methods=['POST'])
def perform_ocr():
    file_to_extract = request.files['uploadedfile']
    file_type = os.path.splitext(file_to_extract.filename)[1]
    if file_type not in ALLOWED_EXTENSIONS:
        return 'Invalid file format, only .png and .pdf allowed!'

    if file_type == '.png':
        image = Image.open(file_to_extract)
        print(image)
        extracted_text = pytesseract.image_to_string(image)
        return extracted_text

    if file_type == '.pdf':
        file_bytes = file_to_extract.read()
        image = convert_from_bytes(file_bytes, fmt="png", transparent=True, single_file=True)
        extracted_text = pytesseract.image_to_string(image[0])
        return extracted_text
    

if __name__ == "__main__":
    app.run(debug=True)