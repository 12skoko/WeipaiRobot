from flask import Flask, request
import requests
import json
import re


class Weipaiing():
    def __init__(self):
        self.works = [[1, '智取威虎山', 0, ''], [2, '芬兰近代银币', 0, ''], [3, '王俭作品', 0, '']]
        self.worksstate = self.works

    def Weipaiing(self, input):
        msg_re = re.compile('(私信?)?(\d+)号?[\.+、，,:：加 ](\d{2})')
        try:
            msg_search = re.findall(msg_re, input[0])
        except:
            return -1
        f = len(msg_search)
        for i in msg_search:
            if int(i[1]) > len(self.works) or int(i[1]) < 1 or int(i[2]) <= 0:
                f -= 1
                continue
            self.worksstate[int(i[1]) - 1][2] = int(i[2]) + self.worksstate[int(i[1]) - 1][2]
            if i[0] != '':
                self.worksstate[int(i[1]) - 1][3] = '匿名'
            else:
                self.worksstate[int(i[1]) - 1][3] = input[1]
        if f == 0:
            print('Null')
            return -1
        return 1

    def Weipaishow(self):
        rstr = ''

        for i in self.worksstate:
            stemp = str(i[0]) + ':' + i[1] + '。' + str(i[2]) + '元,' + i[3] + '\n'
            rstr += stemp

        print(rstr)
        return rstr

app = Flask(__name__)


@app.route('/wxrobot', methods=['POST'])
def wxrobot():
    cbdata=request.form.to_dict()
    print(cbdata)
    input = [cbdata['msg'], cbdata['final_from_name']]
    flag = wppp.Weipaiing(input)

    # data2 = {"type":106,"user_id":"wxid_4v6rvyeygzfq22","message":wppp.Weipaishow(),"msg_type":1,"robot_id":"wxid_11pq0tkx9xk922","token":"12skoko"}
    # data1 = {"type":106,"user_id":"wxid_4v6rvyeygzfq22","message":cbdata['message'],"msg_type":1,"robot_id":"wxid_11pq0tkx9xk922","token":"12skoko"}

    if flag == 1:
        data3 = {"type": 101, "group_id": "19753618745@chatroom", "message": wppp.Weipaishow(), "msg_type": 1,
                 "robot_id": "wxid_11pq0tkx9xk922", "token": "12skoko"}
        rmsg = json.dumps(data3, ensure_ascii=False)
        print(rmsg)
        requests.post('http://127.0.0.1:3800', data=rmsg.encode("utf-8"))
    return '200'


if __name__ == '__main__':
    wppp = Weipaiing()
    app.run(port=5000, debug=True)
