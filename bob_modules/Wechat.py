#!/usr/bin/python
#coding:utf8
import itchat
import requests
import schedule
import time

def toGBK(str):
    str.encode('gbk')
    return str
def getinfo():
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'}
    url = 'http://wthrcdn.etouch.cn/weather_mini?city=%E4%B8%8A%E6%B5%B7'
    sp_url = 'http://wthrcdn.etouch.cn/weather_mini?citykey=101060403'
    r = requests.get(url, headers=headers)
    sp_r = requests.get(sp_url, headers=headers)
    info = (r.json()['data'])
    spinfo = (sp_r.json()['data'])
    sh_info = u"今天是{1}\n\r=== {0} 天气状况 {4} ===\n\r温度 ：{2} ~~ {3} \n\r风向 ：{5}\n\r凤力 ：{6}\n\r{7}".format(info['city'], info['forecast'][0]['date'], info['forecast'][0]['low'], info['forecast'][0]['high'],info['forecast'][0]['type'], info['forecast'][0]['fengxiang'], info['forecast'][0]['fengli'][9:13],info['ganmao'])
    sh_info = toGBK(sh_info)
    sp_info = u"今天是{1}\n\r=== {0}天气状况 {4} ===\n\r温度 ：{2} ~~ {3} \n\r风向 ：{5}\n\r{6}".format(spinfo['city'], spinfo['forecast'][0]['date'], spinfo['forecast'][0]['low'], spinfo['forecast'][0]['high'],spinfo['forecast'][0]['type'], spinfo['forecast'][0]['fengxiang'],spinfo['ganmao'])
    sp_info = toGBK(sp_info)
    return sh_info,sp_info
# friends = itchat.get_friends()
# for i in friends:
#   print (i)

def pushinfo():
    #itchat.send(sh_info, toUserName=lyk)
    itchat.send(sp_info, toUserName=home)
    #itchat.send(sp_info, toUserName=ztc)
   
def loginchat():
    itchat.auto_login(hotReload=True)
def getchat():
    xmk_info = itchat.search_friends(nickName='Coolkid')
    kt_info = itchat.search_friends(name='B')
    beibei_info = itchat.search_friends(nickName='The Future Ver')
    lyk_name = u'嗯哼'
    lyk_info = itchat.search_friends(nickName=lyk_name)
    lyk = lyk_info[0]['UserName']
    homename = u'家庭会'
    ztcname = u'宿爱凡尘'
    home_info = itchat.search_chatrooms(name=homename)
    ztc_info = itchat.search_friends(nickName=ztcname)
    beibei = beibei_info[0]['UserName']
    home = home_info[0]['UserName']
    kt = kt_info[0]['UserName']
    ztc = ztc_info[0]['UserName']
    xmk = xmk_info[0]['UserName']
    return beibei,kt,home
def rest():
    time.sleep(120)
    print('process is running')


if __name__ == '__main__':
    sh_info, sp_info = getinfo()
    itchat.auto_login(hotReload=True)
    beibei,kt,home = getchat()
    #schedule.every(1).day.at("17:44").do(pushinfo)
    schedule.every(20).seconds.do(pushinfo)
    schedule.every(3).minutes.do(loginchat)
    schedule.every(2).minutes.do(rest)
    while True:
        schedule.run_pending()
