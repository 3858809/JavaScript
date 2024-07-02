import os
import time
import asyncio
import base64
import json
import re
import requests
import datetime

from telethon import TelegramClient,sync
from telethon.tl.types import InputMessagesFilterPhotos

#微信提醒
def GetWXMeg(text):
	url = 'http://wxpusher.zjiecode.com/api/send/message'
	data = { 
		'appToken':'AT_OdRi5Z4hzWMr225NfPVHhXVSmfN59GeR', 
		'content':text,  
		'summary':'未响音乐服签到提醒',
		'contentType':1,
		'uids':['UID_8krNXTxaevo6ogJ1g1W3wTnhZpZR'],
		'url':'https%3A%2F%2Fpornemby.club%2Fweb%2Findex.html'
	}
	response = requests.post(url = url, json = data)
	data = response.json()
	return 'ok'

#get通知
def GetPushDeer(text):
    url = "https://api2.pushdeer.com/message/push?pushkey=PDU24090TPIMPFah7knLxVO5Kc9jdjWTyPo1xPDN1&text="+text  # 替换为你想要请求的URL
    response = requests.get(url)
    # 检查请求是否成功
    if response.status_code == 200:
        print("请求成功")
        print(response.text)  # 打印响应内容
    else:
        print("请求失败")

#连续通知
def forGetMeg(text,n):
    for i in range(n):
        GetPushDeer(text)
        GetWXMeg(text)
        time.sleep(5)
        

def setjson(key,text):
	with open("/home/tgqd/qd.json", "r",encoding='utf-8') as jsonFile:
		data = json.load(jsonFile)
	tmp = data[key]
	data[key] = text
	with open("/home/tgqd/qd.json", "w") as jsonFile:
		json.dump(data, jsonFile,ensure_ascii=False)

def getjson(key):
	with open("/home/tgqd/qd.json", "r",encoding='utf-8') as jsonFile:
		data = json.load(jsonFile)
	return data[key]

dqsj = str(datetime.date.today())
print("当前时间：",dqsj)
qdsj = getjson("wxyy") 
print("上次签到时间：",qdsj)
if dqsj in qdsj:
    print("已经签到过！")
else:
    print("今天未响音乐还没有签到过！")
    forGetMeg('今天未响音乐还没有签到过!',5)

print("脚本结束")
