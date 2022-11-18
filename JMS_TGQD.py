import os
import time
import asyncio
import base64
import json
import re
import requests
import datetime
import random

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
channel_link = "jmsembybot"
QDmeg = "/checkin"
#proxy =("socks5","localhost",12345) #不需要代理的话删掉该行
# ==========================================
client = TelegramClient('shexiaoyu',api_id=api_id,api_hash=api_hash,proxy=proxy).start()

API_KEY = 'GWEfyapMzFcjcIjWuktAMn2c' # 自行获取
SECRET_KEY = 'k39i32FaGtVfGvjU4DsamSokzfQ4ww3E'  # 自行获取
OCR_URL = "https://aip.baidubce.com/rest/2.0/ocr/v1/accurate_basic"  # OCR接口
TOKEN_URL = 'https://aip.baidubce.com/oauth/2.0/token'  # TOKEN获取接口

API_KEY_LIST = {0: 'GWEfyapMzFcjcIjWuktAMn2c', 1: '2ASOlMVpLdwEOfe5Aq3nk6Ii'}
SECRET_KEY_LIST = {0: 'k39i32FaGtVfGvjU4DsamSokzfQ4ww3E', 1: '2u6nryrHlrFpGt1ENDiRQfIvacDQlp5Q'}
QDAPI = 0 

def fetch_token():
    global API_KEY
    global SECRET_KEY
    global QDAPI
    API_KEY = API_KEY_LIST[QDAPI]
    SECRET_KEY = SECRET_KEY_LIST[QDAPI]
    # 获取token
    params = {'grant_type': 'client_credentials',
              'client_id': API_KEY,
              'client_secret': SECRET_KEY}
    try:
        f = requests.post(TOKEN_URL, params, timeout=5)
        if f.status_code == 200:
            result = f.json()
            if 'access_token' in result.keys() and 'scope' in result.keys():
                if not 'brain_all_scope' in result['scope'].split(' '):
                    return None, 'please ensure has check the  ability'
                return result['access_token'], ''
            else:
                return None, '请输入正确的 API_KEY 和 SECRET_KEY'
        else:
            return None, '请求token失败: code {}'.format(f.status_code)
    except BaseException as err:
        return None, '请求token失败: {}'.format(err)

def read_file(image_path):
    f = None
    try:
        f = open(image_path, 'rb')  # 二进制读取图片信息
        return f.read(), ''
    except BaseException as e:
        return None, '文件({0})读取失败: {1}'.format(image_path, e)
    finally:
        if f:
            f.close()

def pic2text(img_path):
    def request_orc(img_base, token):
        """
        调用百度OCR接口，图片识别文字
        :param img_base: 图片的base64转码后的字符
        :param token: fetch_token返回的token
        :return: 返回一个识别后的文本字典
        """
        try:
            req = requests.post(
                OCR_URL + "?access_token=" + token,
                data={'image': img_base},
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )
            if req.status_code == 200:
                result = req.json()
                print("result=",result)
                if 'words_result' in result.keys():
                    print("words_result=",req.json()["words_result"])
                    return req.json()["words_result"], ''
                elif 'error_msg' in result.keys():
                    return None, '图片识别失败: {}'.format(req.json()["error_msg"])

            else:
                return None, '图片识别失败: code {}'.format(req.status_code)
        except BaseException as err:
            return None, '图片识别失败: {}'.format(err)

    file_content, file_error = read_file(img_path)
    if file_content:
        token, token_err = fetch_token()
        if token:
            results, result_err = request_orc(base64.b64encode(file_content), token)
            if result_err: # 打印失败信息
                print(result_err)
            for result in results: # 打印处理结果
                return result


#微信提醒
def GetWXMeg(text):
	url = 'http://wxpusher.zjiecode.com/api/send/message'
	data = { 
		'appToken':'AT_OdRi5Z4hzWMr225NfPVHhXVSmfN59GeR', 
		'content':text,  
		'summary':'终点站帐号到期提醒',
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
		return message

		
#识别图片验证码
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

qdsj = getjson("jms")
print("卷毛鼠上一次签到时间：",qdsj)
dqsj = str(datetime.date.today())
print("当前时间：",dqsj)
dqsj_t = datetime.datetime.strptime(dqsj, "%Y-%m-%d")
qdsj_t = datetime.datetime.strptime(qdsj, "%Y-%m-%d")

if dqsj_t > qdsj_t:	
	client.send_message(channel_link, QDmeg) #发送签到命令
while dqsj_t > qdsj_t:
	ddms = random.randint(0,9)
	time.sleep(ddms)
	newmeg = HQXX()
	print("获取的新信息=",newmeg.text)
	if '验证失败' in newmeg.text:
		time.sleep(1)
		client.send_message(channel_link, QDmeg) #发送签到命令
	elif "按顺序点击" in  newmeg.text:
		print("获取到签到信息")
		XZYZM() #下载验证码图片
		##YZM = captcha_solver(channel_link + "/YZM.jpg")
		time.sleep(2)
		YZM = pic2text(channel_link + "/YZM.jpg")
		if YZM == "":
			time.sleep(60)
			client.send_message(channel_link, QDmeg) #发送签到命令
			continue
		YZM = YZM['words'] 
		print("识别的验证码=",YZM)
		print("识别的验证码长度=",len(YZM))
		if len(YZM)<4:
			print("识别准确率差太大跳过本次签到进行新的一次签到")
			time.sleep(60)
			client.send_message(channel_link, QDmeg) #发送签到命令
			continue
		sl = 0
		for j in YZM:
			sfzd = 0
			newmeg2 = HQXX()
			if "验证失败" in newmeg2.text:
				break
			print ("开始点击按钮:",j)
			for button in newmeg.buttons[0]:
				if j in button.text:
					print("匹配按钮文本成功点击按钮:"+j)
					try:
						button.click()
					except:
						print("点击按钮报错")
						break
					sl = sl+1
					sfzd = 1
					break
			for button in newmeg.buttons[1]:
				if j in button.text:
					print("匹配按钮文本成功点击按钮:"+j)
					try:
						button.click()
					except:
						print("点击报错")
						break
					sl = sl+1
					sfzd = 1
					break
			time.sleep(1)
			if sfzd == 0:
				client.send_message(channel_link, QDmeg) #发送签到命令
				break
			print("开始点击下一个按钮")
		
		#client.send_message(channel_link, YZM) #发送签到验证码
		time.sleep(1)
	elif "您距离下次可签到时间" in newmeg.text:
		print("已经签到过")
		setjson("jms",str(datetime.date.today()))
		break
	else:
		time.sleep(60)
		client.send_message(channel_link, QDmeg) #发送签到验证码

client.send_read_acknowledge(channel_link) #将机器人回应设为已读
client.disconnect()
print("脚本结束")
