import random
import time

lenth = 10
string = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"


def getnow():
    now = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    return now


def getpass():
    passwd = []
    for i in range(lenth):
        passwd.append(random.choice(string))
    password = ''.join(passwd)
    return password


nowtime = getnow()
password = getpass()
with open('passwd.txt', 'a') as f:
    f.write(nowtime + ' | ' + 'passwd : ' + password + '\n')
