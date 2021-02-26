import requests
import json


data2 = {
   # "success": True,
  #  "message": "successful!",
    "event": "SendTextMsg",
    "robot_wxid": "wxid_11pq0tkx9xk922",
    "to_wxid": "wxid_4v6rvyeygzfq22",
    "msg": "7775ああsだ"
}
rmsg = json.dumps(data2, ensure_ascii=False).encode('gb2312')

print(rmsg)

requests.post('http://192.168.2.11:8090', data=rmsg)

# msg=se.post('http://192.168.2.12:8072/api.php').text
# print(msg)
