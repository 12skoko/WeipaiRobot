from flask import Flask, request
import requests
import json
import re


# {'type': '200', 'msg_type': '1', 'from_wxid': '19753618745@chatroom', 'final_from_wxid': 'wxid_4v6rvyeygzfq22', 'from_name': '拍卖机器人测试', 'final_from_name': '12skoko', 'robot_wxid': 'wxid_11pq0tkx9xk922', 'msg': '3.20', 'time': '1614322628', 'rid': '10005'}
# {'type': '100', 'msg_type': '1', 'from_wxid': 'wxid_4v6rvyeygzfq22', 'final_from_wxid': 'wxid_4v6rvyeygzfq22', 'from_name': '12skoko ', 'final_from_name': '12skoko ', 'robot_wxid': 'wxid_11pq0tkx9xk922', 'msg': '3.20', 'time': '1614322672', 'rid': '10007'}


class WeipaiingState():
    def __init__(self):
        self.worksstate = []
        self.adminname = ['两江画院', '最爱']
        self.blackname = ['吴小钢']

    def ProcessingBiddingMsg(self, input):
        msg_re = re.compile('(私信?)?(\d+)[号\.+＋十、，,:：。_加 ]+(\d{1,}0)')
        atmsg_re = re.compile('\[@at,nickname=(.*?),wxid=(.*?)\]')
        url_re = re.compile('http')
        try:
            url_search = re.search(url_re, input[0])
        except:
            return -1
        if url_search != None:
            return -1
        if input[1] in self.blackname:
            return -1
        try:
            msg_search = re.findall(msg_re, input[0])
        except:
            return -1
        if input[1] in self.adminname:
            atmsg_search = None
            try:
                atmsg_search = re.search(atmsg_re, input[0])
            except:
                pass
            if atmsg_search != None:
                input[1] = atmsg_search[1]
        f = len(msg_search)
        print(msg_search)
        for i in msg_search:
            if int(i[1]) > len(self.worksstate) or int(i[1]) < 1 or int(i[2]) <= 0:
                f -= 1
                continue
            self.worksstate[int(i[1]) - 1][2] = int(i[2]) + self.worksstate[int(i[1]) - 1][2]
            if i[0] != '':
                self.worksstate[int(i[1]) - 1][3] = '私信'
            else:
                self.worksstate[int(i[1]) - 1][3] = input[1]
        if f == 0:
            return -1
        return 0

    def Changeworksstate(self, input):
        msg_re = re.compile('(\d+)[,，](\d+)[,，]([^,，]*)')
        try:
            msg_search = re.findall(msg_re, input)
        except:
            return -1
        if msg_search == []:
            return -1
        print(msg_search)
        print(self.worksstate)
        for i in msg_search:
            self.worksstate[int(i[0]) - 1][2] = i[1]
            self.worksstate[int(i[0]) - 1][3] = i[2]
        print(self.worksstate)
        return 0

    def BiddingMsgShow(self):
        rstr = '--本次拍品--\n出价方式为阶梯出价，不报总价。\n加价格式：1加xx,1+xx,1号xx\n\n'
        for i in self.worksstate:
            stemp = str(i[0]) + ':' + i[1] + '。' + str(i[2]) + '元，' + i[3] + '\n'
            rstr += stemp
        return rstr


class WeipaiedState():
    def __init__(self):
        self.wxid = ''
        self.works = []
        self.worktemp = []
        self.EDmenustate = 0

    def EDmenu(self):
        if self.EDmenustate == 0:
            rstr = '--当前拍品--\n'
            if self.works == []:
                rstr += '当前没有拍品\n'
            else:
                for i in self.works:
                    stemp = str(i[0]) + '、' + i[1] + '，' + str(i[2]) + '元' + '\n'
                    rstr += stemp
            rstr += '[0]开始拍卖\n'
            rstr += '[1]添加拍品\n'
            rstr += '[2]修改拍品\n'
            rstr += '[3]删除拍品\n'
            rstr += '[4]退出\n'
            return rstr
        elif self.EDmenustate == 11:
            return '输入拍品名称'
        elif self.EDmenustate == 12:
            return '输入起拍价'
        elif self.EDmenustate == 21:
            return '输入拍品序号（输入#不修改）'
        elif self.EDmenustate == 22:
            return '输入拍品名称（输入#不修改）'
        elif self.EDmenustate == 23:
            return '输入起拍价（输入#不修改）'
        elif self.EDmenustate == 31:
            return '输入拍品序号(输入#退出)'

    def ChangeEDMsg(self, input):
        if self.EDmenustate == 0:
            if input == '0':
                return 2
            if input == '1':
                self.EDmenustate = 11
                return 0
            elif input == '2':
                self.EDmenustate = 21
                return 0
            elif input == '3':
                self.EDmenustate = 31
                return 0
            elif input == '4':
                return 1
            else:
                return -1

        elif self.EDmenustate == 11:
            self.worktemp.append(len(self.works) + 1)
            self.worktemp.append(input)
            self.EDmenustate = 12
            return 0
        elif self.EDmenustate == 12:
            self.worktemp.append(int(input))
            self.works.append(self.worktemp)
            self.EDmenustate = 0
            self.worktemp = []
            return 0

        elif self.EDmenustate == 21:
            if input == '#':
                self.EDmenustate = 0
                return 0
            elif int(input) > 0 and int(input) <= len(self.works):
                self.worktemp.append(int(input))
                self.EDmenustate = 22
                return 0
            else:
                return -1
        elif self.EDmenustate == 22:
            if input == '#':
                self.worktemp.append(self.works[self.worktemp[0] - 1][1])
            else:
                self.worktemp.append(input)
            self.EDmenustate = 23
            return 0
        elif self.EDmenustate == 23:
            if input == '#':
                self.worktemp.append(self.works[self.worktemp[0] - 1][2])
            else:
                self.worktemp.append(int(input))
            self.works[self.worktemp[0] - 1] = self.worktemp
            self.EDmenustate = 0
            self.worktemp = []
            return 0

        elif self.EDmenustate == 31:
            if input == '#':
                self.EDmenustate = 0
                return 0
            elif int(input) > 0 and int(input) <= len(self.works):
                del self.works[int(input) - 1]
                for i in self.works:
                    if i[0] > int(input):
                        i[0] -= 1
                self.EDmenustate = 0
                return 0
            else:
                return -1


class Weipai(WeipaiedState, WeipaiingState):

    def __init__(self):

        self.state = 0  # 0 未拍卖  # 1 正在拍卖
        self.TTmenustate = 0
        self.rdata = [0, '', '']
        self.admin = ['wxid_2zjxs3mstzcl22', 'wxid_4v6rvyeygzfq22', 'wxid_x0wbwe46exmy21']
        # self.admin = ['wxid_2zjxs3mstzcl22', 'wxid_x0wbwe46exmy21']

        # self.chatroom = '3024499764@chatroom'
        self.chatroom = '19753618745@chatroom'
        self.chatroomg = ['19753618745@chatroom', '3024499764@chatroom', '80916718@chatroom']
        WeipaiedState.__init__(self)
        WeipaiingState.__init__(self)

    def rpost(self):
        if type(self.rdata[0]) != type([]):
            if self.rdata[0] == 0:
                data2 = {"type": 106, "user_id": self.rdata[1], "message": self.rdata[2], "msg_type": 1,
                         "robot_id": "wxid_11pq0tkx9xk922",
                         "token": "12skoko"}
                rpoststr = json.dumps(data2, ensure_ascii=False).encode("utf-8")
            else:
                data3 = {"type": 101, "group_id": self.rdata[1], "message": self.rdata[2], "msg_type": 1,
                         "robot_id": "wxid_11pq0tkx9xk922",
                         "token": "12skoko"}
                rpoststr = json.dumps(data3, ensure_ascii=False).encode("utf-8")
            return rpoststr
        else:
            rpoststr = []
            for i in self.rdata:
                if i[0] == 0:
                    data2 = {"type": 106, "user_id": i[1], "message": i[2], "msg_type": 1,
                             "robot_id": "wxid_11pq0tkx9xk922",
                             "token": "12skoko"}
                    rpoststr.append(json.dumps(data2, ensure_ascii=False).encode("utf-8"))
                else:
                    data3 = {"type": 101, "group_id": i[1], "message": i[2], "msg_type": 1,
                             "robot_id": "wxid_11pq0tkx9xk922",
                             "token": "12skoko"}
                    rpoststr.append(json.dumps(data3, ensure_ascii=False).encode("utf-8"))
            return rpoststr

    def TTmenu(self):
        if self.TTmenustate == 0:
            return '--当前未在拍卖--\n[0]开始拍卖\n[1]查看拍品\n'
        if self.TTmenustate == 10:
            rstr = '本次拍品共有' + str(len(self.works)) + '件\n[0]开始拍卖\n[1]返回菜单\n'
            return rstr

    def ProcessingMsg(self, cbdata):
        if self.state == 0 and cbdata['type'] == '100' and cbdata['final_from_wxid'] in self.admin:
            if self.TTmenustate == 0:
                if cbdata['msg'] == '菜单':
                    self.rdata = [0, cbdata['final_from_wxid'], self.TTmenu()]
                    return 1
                elif cbdata['msg'] == '1':
                    self.wxid = cbdata['final_from_wxid']
                    self.TTmenustate = 11
                    self.rdata = [0, cbdata['final_from_wxid'], self.EDmenu()]
                    return 1
                elif cbdata['msg'] == '0':
                    if len(self.works) == 0:
                        self.rdata = [0, cbdata['final_from_wxid'], '没有拍卖品']
                        return 1
                    else:
                        self.TTmenustate = 10
                        self.rdata = [0, cbdata['final_from_wxid'], self.TTmenu()]
                        return 1
                else:
                    return 0
            elif self.TTmenustate == 11:
                if self.wxid == cbdata['final_from_wxid']:
                    input = cbdata['msg']
                    flag = self.ChangeEDMsg(input)
                    if flag == -1:
                        return 0
                    elif flag == 0:
                        self.rdata = [0, cbdata['final_from_wxid'], self.EDmenu()]
                        return 1
                    elif flag == 1:
                        self.TTmenustate = 0
                        self.rdata = [0, cbdata['final_from_wxid'], self.TTmenu()]
                        return 1
                    elif flag == 2:
                        if len(self.works) == 0:
                            self.rdata = [0, cbdata['final_from_wxid'], '没有拍卖品']
                            return 1
                        else:
                            self.TTmenustate = 10
                            self.rdata = [0, cbdata['final_from_wxid'], self.TTmenu()]
                            return 1
                else:
                    self.rdata = [0, cbdata['final_from_wxid'], '当前菜单正在被使用']
                    return 1
            elif self.TTmenustate == 10:
                if cbdata['msg'] == '0':
                    self.state = 1
                    self.TTmenustate = 0
                    self.worksstate = self.works
                    for i in self.worksstate:
                        i.append('')
                    self.rdata = [[0, self.chatroom, '拍卖开始！'], [0, cbdata['final_from_wxid'], '拍卖开始'],
                                  [0, self.chatroom, self.BiddingMsgShow()]]
                    return 1
                elif cbdata['msg'] == '1':
                    self.TTmenustate = 0
                    self.rdata = [0, cbdata['final_from_wxid'], self.TTmenu()]
                    return 1
                else:
                    return 0
            else:
                return 0
        elif self.state == 1 and cbdata['final_from_wxid'] in self.admin and cbdata['msg'] == '成交':
            self.rdata = [[0, 'wxid_x0wbwe46exmy21', self.BiddingMsgShow()], [0, self.chatroom, '本次拍卖结束，感谢大家参与！'],
                          [0, cbdata['final_from_wxid'], '拍卖结束'], [0, 'wxid_2zjxs3mstzcl22', self.BiddingMsgShow()]]
            # self.rdata = [[0, self.chatroom, '本次拍卖结束，感谢大家参与！'],
            # [0, cbdata['final_from_wxid'], '拍卖结束']]
            self.worksstate = []
            self.worksstate = []
            self.works = []
            self.state = 0
            return 1
        elif self.state == 1 and cbdata['type'] == '200':
            input = [cbdata['msg'], cbdata['final_from_name']]
            flag = self.ProcessingBiddingMsg(input)
            if flag == 0:
                self.rdata = [0, self.chatroom, self.BiddingMsgShow()]
                return 1
            else:
                return 0
        elif self.state == 1 and cbdata['type'] == '100' and cbdata['final_from_wxid'] in self.admin:
            flag = self.Changeworksstate(cbdata['msg'])
            if flag == 0:
                self.rdata = [[0, self.chatroom, self.BiddingMsgShow()], [0, cbdata['final_from_wxid'], '修改成功']]
                return 1
            else:
                return 0

        elif cbdata['type'] == '410' and cbdata['from_wxid'] in self.chatroomg:
            mem_re = re.compile('"member_nickname":"(.*?)".*?"group_name":"(.*?)"')
            mem_search = re.search(mem_re, cbdata['msg'])
            rstr = mem_search[1] + '退出' + mem_search[2]
            self.rdata = [[0, 'wxid_x0wbwe46exmy21', rstr], [0, 'wxid_2zjxs3mstzcl22', rstr]]
            return 1
        else:
            return 0


app = Flask(__name__)


@app.route('/wxrobot', methods=['POST'])
def wxrobot():
    # req_str = request.form[0:int(request.cont)]
    # req_data = json.loads(req_str, encoding='utf-8')

    cbdata = request.form.to_dict()

    if cbdata == {}:
        return 'refrash', 204

    print(cbdata)
    flag = wppp.ProcessingMsg(cbdata)

    # data2 = {"type":106,"user_id":"wxid_4v6rvyeygzfq22","message":wppp.Weipaishow(),"msg_type":1,"robot_id":"wxid_11pq0tkx9xk922","token":"12skoko"}
    # data1 = {"type":106,"user_id":"wxid_4v6rvyeygzfq22","message":cbdata['message'],"msg_type":1,"robot_id":"wxid_11pq0tkx9xk922","token":"12skoko"}

    if flag == 1:
        rpoststr = wppp.rpost()
        if type(rpoststr) != type([]):
            print(rpoststr.decode())
            requests.post('http://127.0.0.1:3800', data=rpoststr)
        else:
            for i in rpoststr:
                print(i.decode())
                requests.post('http://127.0.0.1:3800', data=i)
    return 'ok', 200


if __name__ == '__main__':
    wppp = Weipai()
    app.run(port=5000, debug=True)
