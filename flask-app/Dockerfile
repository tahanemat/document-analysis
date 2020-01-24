FROM python:3.7.6-stretch

COPY . /usr/src/app

WORKDIR /usr/src/app

RUN apt-get update && apt-get install tesseract-ocr -y

RUN python3 -m pip install -r requirements.txt

EXPOSE 5000

ENTRYPOINT [ "python3" ]

CMD [ "init.py" ]