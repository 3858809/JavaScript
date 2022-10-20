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
proxy = None
# =============需要被替换的值=================
'''
api_id 你的api id
api_hash 你的api hash
channel_link 要下载图片的频道链接
proxy 将localhost改成代理地址,12345改成代理端口
picture_storage_path 图片下载到的路径
'''
api_id = 5672799
api_hash = "e08529171140eac69071c630f03f1a7a"
channel_link = "polo_emby_bot"
QDmeg = "/info"
#proxy =("socks5","localhost",12345) #不需要代理的话删掉该行
# ==========================================
client = TelegramClient('shexiaoyu',api_id=api_id,api_hash=api_hash,proxy=proxy).start()

#微信提醒
def GetWXMeg(text):
	url = 'http://wxpusher.zjiecode.com/api/send/message'
	data = { 
		'appToken':'AT_OdRi5Z4hzWMr225NfPVHhXVSmfN59GeR', 
		'content':text,  
		'summary':'polo自动查看异常提醒',
		'contentType':1,
		'uids':['UID_8krNXTxaevo6ogJ1g1W3wTnhZpZR'],
		'url':'https%3A%2F%2Fpornemby.club%2Fweb%2Findex.html'
	}
	response = requests.post(url = url, json = data)
	data = response.json()
	return 'ok'

#下载验证码图片
def XZYZM():
	photos = client.get_messages(channel_link, None, filter=InputMessagesFilterPhotos)
	index = 0
	for photo in photos:
		filename = channel_link + "/YZM.jpg"
		index = index + 1
		if index == 1:
			client.download_media(photo, filename)
		break
	print("下载完毕")

def HQXX():
	for message in client.iter_messages(channel_link):
		return message.text
def captcha_solver(f):
	with open(f, "rb") as image_file:
		encoded_string = base64.b64encode(image_file.read()).decode('ascii')
		url = 'https://api.apitruecaptcha.org/one/gettext'
		data = { 
			'userid':'sheriqiang@gmail.com', 
			'apikey':'L7GYXVaB2BreQrGhzh3I',  
			'data':encoded_string
		}
		response = requests.post(url = url, json = data)
		data = response.json()
		return data['result']
	
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

client.send_message(channel_link, QDmeg) #发送签到命令
time.sleep(3)
newmeg = HQXX()
text = newmeg.split('最近活动: ')[1]
print("text=",text)
hdsj =  text.split('注册日期: ')[0] 
print("最后活动时间=",hdsj)
dqsj = str(datetime.date.today())
print("当前时间=",dqsj)
hdsj_t = datetime.datetime.strptime(hdsj, "%Y-%m-%d")
dqsj_t = datetime.datetime.strptime(dqsj, "%Y-%m-%d")
print("剩余天数=",day)
if dqsj_t > qdsj_t:
	GetWXMeg('polo最后活动时间:' + hdsj + ',请检查自动观看是否还正常')

client.send_read_acknowledge(channel_link) #将机器人回应设为已读
client.disconnect()
print("脚本结束")
