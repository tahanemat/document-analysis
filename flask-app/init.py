from flask import Flask,render_template, request, Response
from PIL import Image
from pdf2image import convert_from_bytes
import pytesseract
import pika
import os
import time
app = Flask(__name__)

ALLOWED_EXTENSIONS = ['.pdf','.png']

connected = False

while connected == False:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
        channel = connection.channel()
        channel.queue_declare(queue='extracted')
        connected = True
        print('connection successful')
    except Exception as e:
        print('connection failed because ' + str(e))
        time.sleep(3)


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/submit_file', methods=['POST'])
def perform_ocr():
    file_to_extract = request.files['file']
    file_type = os.path.splitext(file_to_extract.filename)[1]
    if file_type not in ALLOWED_EXTENSIONS:
        return 'Invalid file format, only .png and .pdf allowed!'

    if file_type == '.png':
        image = Image.open(file_to_extract)
        extracted_text = pytesseract.image_to_string(image)
        channel.basic_publish(exchange='', routing_key='extract', body=extracted_text)
        return ('', 204)

    if file_type == '.pdf':
        file_bytes = file_to_extract.read()
        image = convert_from_bytes(file_bytes, fmt="png", transparent=True, single_file=True)
        extracted_text = pytesseract.image_to_string(image[0])
        channel.basic_publish(exchange='', routing_key='extract', body=extracted_text)
        print(extracted_text)
        return ('', 204)


def event_stream(rec_channel):
    for method, properties, body in rec_channel.consume(queue='result', auto_ack=True):
        yield 'data: %s\n\n' % body

@app.route('/stream')
def stream():
    rec_connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    rec_channel = rec_connection.channel()
    rec_channel.queue_declare(queue='result')
    return Response(event_stream(rec_channel),mimetype="text/event-stream")

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')