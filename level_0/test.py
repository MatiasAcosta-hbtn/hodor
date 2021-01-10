#!/usr/bin/python3
import requests


url = "http://158.69.76.135/level0.php"
data_key = {"id":"2278", "holdthedoor":"Submit+Query"}
headers_key = {"user_agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64)"}

for i in range(10):
    try:
        requests.post(url, data = data_key, headers = headers_key)
        print("success")
    except:
        print("fail")
