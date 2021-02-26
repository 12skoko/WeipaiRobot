from flask import Flask, request
import requests
import json

app = Flask(__name__)


@app.route('/wxrobot', methods=['POST'])
def wxrobot():
    data=request.form.to_dict()
    if data['type']==100:





        se=requests.session()
        data1 =  { 'type' : 100, 'msg' : data['msg'], 'to_wxid' : data['from_wxid'],'robot_wxid':'wxid_11pq0tkx9xk922'}

        rmsg=json.dumps(data1)
        print(rmsg)
        se.post('http://192.168.2.12:8073/send',data=rmsg)



if __name__ == '__main__':
    app.run(port=5000, debug=True)
