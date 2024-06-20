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
channel_link = "EmbyMistyBot"
fj_link = "FreeEmbyNotice"
QDmeg = "🛎每日签到"

ZCmeg = "⚡️注册账号"
ZHM = "shexiaoyu"
ZHMM = "s3858809"

TCapikey={
	"sheriqiang@gmail.com":"L7GYXVaB2BreQrGhzh3I",
	"s3858809":"dPwkV7LPndiZmn2rHp81",
	"shexiaoyu":"cLiDO6dflOthLre2fqKb",
	"linyinfei":"ZKWyX71qkCZu25e7AfNO",
	"linchunmiao":"NBX1A27nDnD0NcqlR3fq",
	"xiaochunmiaoyaya2":"jG6O4aUjeaSxrgL07J18",
	"xishi":"7dDVX4Lgl8adm9aQxHEU"
}

#proxy =("socks5","localhost",12345) #不需要代理的话删掉该行
# ==========================================
client = TelegramClient('shexiaoyu',api_id=api_id,api_hash=api_hash,proxy=proxy).start()

#微信提醒
def GetWXMeg(text):
	url = 'http://wxpusher.zjiecode.com/api/send/message'
	data = { 
		'appToken':'AT_OdRi5Z4hzWMr225NfPVHhXVSmfN59GeR', 
		'content':text,  
		'summary':'考研服帐号到期提醒',
		'contentType':1,
		'uids':['UID_8krNXTxaevo6ogJ1g1W3wTnhZpZR'],
		'url':'https%3A%2F%2Fpornemby.club%2Fweb%2Findex.html'
	}
	response = requests.post(url = url, json = data)
	data = response.json()
	return 'ok'

#下载验证码图片
def XZYZM():
	print("开始获取频道photos")
	#photos = client.get_messages(channel_link, None, filter=InputMessagesFilterPhotos)
	print("获取完毕")
	index = 0
	for photo in client.iter_messages(channel_link, None, filter=InputMessagesFilterPhotos):
	#for photo in photos:
		filename = channel_link + "/YZM.jpg"
		index = index + 1
		if index == 1:
			print("开始下载最新的一张图片")
			client.download_media(photo, filename)
			print("下载完毕")
		break
	print("退出下载")

def HQXX():
	for message in client.iter_messages(channel_link):
		return message

def FJXX():
	for message in client.iter_messages(fj_link):
		return message

def captcha_solver(f):
	for key in TCapikey :
		print("开始进行验证码识别，使用账号：")
		print("userid=",key)
		print("key=",TCapikey[key])
		with open(f, "rb") as image_file:
			encoded_string = base64.b64encode(image_file.read()).decode('ascii')
			url = 'https://api.apitruecaptcha.org/one/gettext'
			data = { 
				'userid':key, 
				'apikey':TCapikey[key],  
				'data':encoded_string
			}
			response = requests.post(url = url, json = data)
			data = response.json()
			print("data=",data)
			if "result" in data:
				return data['result']
			else :
				print("账号免费数量用完：",key)
	
	print("全部账号的免费数量都用完了")	
	
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

YZM = input("请输入验证码: ")

syc_fjmeg = FJXX()
print("最后一次封号信息:",syc_fjmeg.text)

esc = 0 
while esc == 0:
    time.sleep(1)
    #获取新的封号信息
    new_fjmeg = FJXX()
    if new_fjmeg.text != syc_fjmeg.text:
        # 有新的帐号被封了
        print("有新的帐号被封了,开始抢注...")
        print("发送注册验证码=",YZM)
        client.send_message(channel_link, YZM) #发送签到验证码
        s_yhm = 0 
        while s_yhm==0:
            newmeg = HQXX()
            print("获取的新信息=",newmeg.text)
            #🧸现在, 请输入您的账号 (4~12位 可用: 字母, 数字, 下划线, 输入 /cancel 取消):
            if "账号" in newmeg.text:
                print("开始输入用户名")
                client.send_message(channel_link, ZHM) #发送用户名
                s_yhm=1
            else:
                print("等待用户名信息")
                
        s_mm = 0 
        while s_mm==0:
            newmeg = HQXX()
            print("获取的新信息=",newmeg.text)
            #🤫现在, 请输入您的密码 (4~12位 可用: 字母, 数字, 下划线, 输入 /cancel 取消将使用空密码):
            if "密码" in newmeg.text:
                print("开始输入改密")
                client.send_message(channel_link, ZHMM) #发送改密
                s_mm=1
            else:
                print("等待该密信息")
            
        
        print("抢号流程结束了")
        GetWXMeg("抢号流程结束了")
        
    else:
        print("等待有人被封号..")

client.send_read_acknowledge(channel_link) #将机器人回应设为已读
client.disconnect()
print("脚本结束")
