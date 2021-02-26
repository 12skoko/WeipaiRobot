import re


def Weipaiing(input, wpingState, state):
    msg_re = re.compile('(\d*)号?[\.+、，,加](\d*)')
    msg_search = re.search(msg_re, input[0])
    if msg_search == None:
        return -1
    if int(msg_search[1]) > len(state) or int(msg_search[2]) <= 0:
        return -1

    wpingState_temp = [0, '']
    wpingState_temp[0] = int(msg_search[2]) + wpingState[0]
    wpingState_temp[1] = input[1]

    return wpingState_temp

def Weipai(state):
    pass

state = [[1], [2]]
input = ['1加200', '12skoko']
wpingState = [500, 'skoko12']
print(wpingState)
rState = Weipaiing(input, wpingState, state)
if rState != -1:
    wpingState = rState
print(wpingState)
