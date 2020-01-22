from flask import Flask,render_template, request
import pytesseract
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_file', methods = ['POST'])
def perform_ocr():
    file_to_extract = request.form['filename']
    return 'file submitted'


if __name__ == "__main__":
    app.run(debug=True)