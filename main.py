from flask import Flask, request
import requests
import json
import re


# {'type': '200', 'msg_type': '1', 'from_wxid': '19753618745@chatroom', 'final_from_wxid': 'wxid_4v6rvyeygzfq22', 'from_name': '拍卖机器人测试', 'final_from_name': '12skoko', 'robot_wxid': 'wxid_11pq0tkx9xk922', 'msg': '3.20', 'time': '1614322628', 'rid': '10005'}
# {'type': '100', 'msg_type': '1', 'from_wxid': 'wxid_4v6rvyeygzfq22', 'final_from_wxid': 'wxid_4v6rvyeygzfq22', 'from_name': '12skoko ', 'final_from_name': '12skoko ', 'robot_wxid': 'wxid_11pq0tkx9xk922', 'msg': '3.20', 'time': '1614322672', 'rid': '10007'}


class WeipaiingState():
    def __init__(self):
        self.works = [[1, '智取威虎山', 0, ''], [2, '芬兰近代银币', 0, ''], [3, '王俭作品', 0, '']]
        self.worksstate = self.works

    def ProcessingBiddingMsg(self, input):
        msg_re = re.compile('(私信?)?(\d+)[号\.+、，,:：加 ](\d{2})')
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

    def BiddingMsgShow(self):
        rstr = ''

        for i in self.worksstate:
            stemp = str(i[0]) + ':' + i[1] + '。' + str(i[2]) + '元,' + i[3] + '\n'
            rstr += stemp

        print(rstr)
        return rstr

class WeipaiedState():
    def __init__(self):
        self.works=[]
        self.worktemp=[]
        self.menustate=0
    def menu(self):
        if self.menustate == 0:
            rstr='--当前拍品--\n'
            if self.works==[]:
                rstr+='当前没有拍品\n'
            else:
                for i in self.works:
                    stemp = str(i[0]) + '、' + i[1] + ',' + str(i[2]) + '元' + '\n'
                    rstr += stemp
            rstr += '[0]开始拍卖\n'
            rstr += '[1]添加拍品\n'
            rstr += '[2]修改拍品\n'
            rstr += '[3]删除拍品\n'
            rstr += '[4]退出\n'
            return rstr
        elif self.menustate==11:
            return '输入拍品名称'
        elif self.menustate==12:
            return '输入起拍价'
        elif self.menustate==21:
            return '输入拍品序号（输入#不修改）'
        elif self.menustate==22:
            return '输入拍品名称（输入#不修改）'
        elif self.menustate==23:
            return '输入起拍价（输入#不修改）'
        elif self.menustate==31:
            return '输入拍品序号(输入#退出)'
    def ProcessingChangeMsg(self,input):
        if self.menustate == 0:
            if input == '0':
                pass
                return 1
            elif input == '1':
                self.menustate=11
                return 0
            elif input == '2':
                self.menustate=21
                return 0
            elif input == '3':
                self.menustate=31
                return 0
            else:
                return -1

        elif self.menustate ==11:
            self.worktemp.append(len(self.works)+1)
            self.worktemp.append(input)
            self.menustate=12
            return 0
        elif self.menustate == 12:
            self.worktemp.append(int(input))
            self.works.append(self.worktemp)
            self.menustate = 0
            self.worktemp=[]
            return 0

        elif self.menustate == 21:
            if input=='#':
                self.menustate=0
                return 0
            elif int(input)>0 and int(input)<=len(self.works):
                self.worktemp.append(int(input))
                self.menustate =22
                return 0
            else:
                return -1
        elif self.menustate == 22:
            if input=='#':
                self.worktemp.append(self.works[self.worktemp[0]-1][1])
            else:
                self.worktemp.append(input)
            self.menustate =23
            return 0
        elif self.menustate == 23:
            if input=='#':
                self.worktemp.append(self.works[self.worktemp[0]-1][2])
            else:
                self.worktemp.append(int(input))
            self.works[self.worktemp[0]-1]=self.worktemp
            self.menustate =0
            self.worktemp=[]
            return 0

        elif self.menustate==31:
            if input=='#':
                self.menustate=0
                return 0
            elif int(input) > 0 and int(input) <= len(self.works):
                del self.works[int(input)-1]
                for i in self.works:
                    if i[0]>int(input):
                        i[0]-=1
                self.menustate =0
                return 0
            else:
                return -1






class Weipai(WeipaiedState):

    def __init__(self):


        self.state = [0]  # 0 未拍卖  # 1 正在拍卖
        WeipaiedState.__init__(self)
    def ProcessingMsg(self, cbdata):
        if self.state == 0:
            if cbdata['type'] == 100 and (cbdata['final_from_wxid'] == 'wxid_4v6rvyeygzfq22'):
                pass

        elif self.state == 1:
            pass















app = Flask(__name__)


@app.route('/wxrobot', methods=['POST'])
def wxrobot():
    cbdata = request.form.to_dict()

    flag = wppp.ProcessingChangeMsg(cbdata['msg'])

    # data2 = {"type":106,"user_id":"wxid_4v6rvyeygzfq22","message":wppp.Weipaishow(),"msg_type":1,"robot_id":"wxid_11pq0tkx9xk922","token":"12skoko"}
    # data1 = {"type":106,"user_id":"wxid_4v6rvyeygzfq22","message":cbdata['message'],"msg_type":1,"robot_id":"wxid_11pq0tkx9xk922","token":"12skoko"}

    if 1:
        data3 = {"type": 101, "group_id": "19753618745@chatroom", "message": wppp.menu(), "msg_type": 1,
                 "robot_id": "wxid_11pq0tkx9xk922", "token": "12skoko"}
        rmsg = json.dumps(data3, ensure_ascii=False)
        print(rmsg)
        requests.post('http://127.0.0.1:3800', data=rmsg.encode("utf-8"))
    return '200'


if __name__ == '__main__':
    wppp = Weipai()
    app.run(port=5000, debug=True)
