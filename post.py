import time
import requests
while True:
    re=requests.session()
    re.post('http://127.0.0.1:5000/wxrobot')
    time.sleep(2)