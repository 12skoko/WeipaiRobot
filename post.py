import time
import requests
while True:
    re=requests.session()
    print(re.post('http://127.0.0.1:5000/wxrobot').status_code)
    time.sleep(600)