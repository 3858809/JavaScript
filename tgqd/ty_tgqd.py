
from telethon import TelegramClient, events
from telethon.tl.functions.messages import SendMessageRequest
from telethon.tl.functions.messages import GetBotCallbackAnswerRequest
import asyncio
import logging
import configparser
from PIL import Image
import pytesseract
import io
import requests
import re
from datetime import datetime, timedelta

# 配置日志
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# 读取配置文件
config = configparser.ConfigParser()
config.read('/home/tgqd/config.ini')

# 获取全局配置
API_ID = config.get('Telegram', 'API_ID')
API_HASH = config.get('Telegram', 'API_HASH')
PHONE_NUMBER = config.get('Telegram', 'PHONE_NUMBER')
PUSHDEER_KEY = config.get('PushDeer', 'PUSHDEER_KEY')  # PushDeer 的 PushKey

# 初始化 Telegram 客户端
client = TelegramClient('session_name', API_ID, API_HASH)

async def check_manual_signin_reminder(event, bot_entity, bot_rules):
    """
    提醒未响音乐服手动签到
    """
    try:
        # 使用正则表达式匹配上次签到时间
        message_text = event.message.message
        logger.info(f"未响音乐服上一次签到时间获取...")
        last_signin_pattern = r"上次签到时间[：:](\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
        match = re.search(last_signin_pattern, message_text)

        if match:
            last_signin_time = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
            logger.info(f"未响音乐服上一次签到时间:{last_signin_time}")
            days_since_last_signin = (datetime.now() - last_signin_time).days

            if days_since_last_signin > 7:
                await send_pushdeer_notification(
                    f"未响音乐已 {days_since_last_signin} 天未签到",
                    f"您已 {days_since_last_signin} 天未签到，请及时签到以避免惩罚！"
                )
            logger.info(f"未响音乐服手动签到提醒: 已 {days_since_last_signin} 天未签到")
        else:
            # 如果未识别到上次签到时间，发送提醒
            await send_pushdeer_notification(
                "未响音乐服手动签到提醒",
                "无法识别上次签到时间，请检查机器人消息格式或手动确认签到状态。"
            )
            logger.warning("未识别到上次签到时间，已发送提醒")
            
        logger.info(f"未响音乐服上一次听歌时间获取...")
        # 发送 /start 命令
        await client(SendMessageRequest(
            peer=bot_entity,
            message="/start"
        ))
        logger.info(f"已向 {bot_entity.username} 发送 /start 命令")
        
        # 等待机器人回复
        await asyncio.sleep(8)
        
        # 点击按钮 帳戶資訊
        async for message in client.iter_messages(bot_entity, limit=1):
            for row in message.reply_markup.rows:
                for button in row.buttons:
                    if "帳戶資訊" in button.text:
                        logger.info(f"点击按钮【帳戶資訊】")
                        logger.info(f"按钮内容: {button}")
                        try:
                            logger.info(f"点击按钮【{button.text}】")
                            response = await client(GetBotCallbackAnswerRequest(
                                peer=message.peer_id,
                                msg_id=message.id,
                                data=button.data
                            ))
                            logger.info(f"回调响应: {response}")
                        except Exception as e:
                            logger.error(f"回调失败: {e}")
                        logger.info(f"已点击按钮: {button.text}")
                        break
        
        # 获取“帳戶資訊”后的回复信息
        await asyncio.sleep(5)
        
        async for message in client.iter_messages(bot_entity, limit=1):
            logger.info(f"开始提取信息")
            logger.info(f"message.message：{message.message}")
            navidrome_pattern = r"Navidrome 最近登陸時間:\s*([\d\-T:.Z]+)"
            navidrome_match = re.search(navidrome_pattern, message.message)
        
            if navidrome_match:
                # 去掉毫秒部分和末尾 'Z'，只取前面的标准时间格式
                time_str = navidrome_match.group(1).split('.')[0]  # 切掉毫秒部分
                time_str = time_str.replace('T', ' ').replace('Z', '')  # 替换 'T' 并去掉 'Z'
                last_navidrome_time = datetime.strptime(time_str, "%Y-%m-%d %H:%M:%S")
                logger.info(f"未响音乐服上一次听歌时间:{last_navidrome_time}")
                days_since_last_navidrome = (datetime.now() - last_navidrome_time).days
        
                if days_since_last_navidrome > 7:
                    await send_pushdeer_notification("未响音乐未登录已过去 {days_since_last_navidrome} 天", f"上一次未响音乐登录时间为 {last_navidrome_time}，距离上次已过去 {days_since_last_navidrome} 天，请尽快登录避免惩罚！")
                logger.warning(f"上一次未响音乐登录时间为 {last_navidrome_time}，距离上次已过去 {days_since_last_navidrome} 天，请尽快登录避免惩罚！")
        
                # 删除这条信息
                await client.delete_messages(bot_entity, message.id)
                logger.info("已删除查看登录时间信息")
                    
    except Exception as e:
        logger.error(f"未响音乐服签到提醒失败: {e}")

async def solve_captcha(image_data):
    """
    识别图片验证码
    :param image_data: 图片的二进制数据
    :return: 识别到的验证码文本
    """
    try:
        # 将图片数据转换为 PIL 图像
        image = Image.open(io.BytesIO(image_data))
        # 使用 Tesseract OCR 识别验证码
        captcha_text = pytesseract.image_to_string(image, config='--psm 8')
        logger.info(f"识别到的验证码: {captcha_text}")
        return captcha_text.strip()
    except Exception as e:
        logger.error(f"验证码识别失败: {e}")
        return None

async def send_pushdeer_notification(title, message):
    """
    通过 PushDeer 发送通知
    :param title: 通知标题
    :param message: 通知内容
    """
    try:
        url = "https://api2.pushdeer.com/message/push"
        payload = {
            "pushkey": PUSHDEER_KEY,
            "text": title,
            "desp": message,
            "type": "markdown"
        }
        response = requests.post(url, data=payload)
        if response.status_code == 200:
            logger.info("PushDeer 通知发送成功！")
        else:
            logger.error(f"PushDeer 通知发送失败: {response.text}")
    except Exception as e:
        logger.error(f"PushDeer 通知发送异常: {e}")

def parse_expiry_date(message_text):
    """
    从消息文本中解析过期时间
    :param message_text: 机器人的回复消息文本
    :return: 过期时间（datetime 对象），如果未找到则返回 None
    """
    try:
        # 使用正则表达式匹配日期（格式：YYYY-MM-DD 或 YYYY年MM月DD日）
        date_pattern = r"(\d{4}-\d{2}-\d{2})|(\d{4}年\d{2}月\d{2}日)"
        match = re.search(date_pattern, message_text)
        if match:
            date_str = match.group(0)
            # 统一转换为 YYYY-MM-DD 格式
            if "年" in date_str:
                date_str = date_str.replace("年", "-").replace("月", "-").replace("日", "")
            return datetime.strptime(date_str, "%Y-%m-%d")
        return None
    except Exception as e:
        logger.error(f"解析过期时间失败: {e}")
        return None

async def handle_bot_message(event,bot_username, bot_rules):
    """
    处理机器人回复消息
    :param event: 机器人回复消息事件
    :param bot_rules: 当前机器人的规则列表
    """
    # 查找签到机器人
    bot_entity = await client.get_entity(bot_username)
    message_text = event.message.message
    logger.info(f"收到消息: {message_text}")

	# 打印按钮信息（调试用）
    if event.message.reply_markup:
        for row in event.message.reply_markup.rows:
            for button in row.buttons:
                logger.info(f"发现按钮: {button.text}")

    # 遍历机器人的规则
    for rule in bot_rules:
        logger.info(rule)
        pattern = rule.get('pattern')
        action = rule.get('action')
        response = rule.get('response', '')
        notify_days = rule.get('notify_days', None)  # 获取提醒天数配置

        # 检查是否匹配规则
        if re.search(pattern, message_text, re.IGNORECASE):
            logger.info(f"匹配到规则: {pattern} -> {action}")

            if action == "click_button":
                # 点击按钮
                if event.message.reply_markup:
                    for row in event.message.reply_markup.rows:
                        for button in row.buttons:
                            if re.search(response, button.text, re.IGNORECASE):
                                try:
                                    result = await client(GetBotCallbackAnswerRequest(
                                        peer=event.message.peer_id,
                                        msg_id=event.message.id,
                                        data=button.data
                                    ))
                                    logger.info(f"已点击按钮: {button.text}")
                                    await asyncio.sleep(5)  # 等待响应，确保消息被处理

                                    # 检查点击按钮后的新消息
                                    if result and hasattr(result, 'updates'):
                                        for update in result.updates:
                                            if hasattr(update, 'message'):
                                                logger.info(f"按钮点击后收到消息: {update.message.message}")
                                except Exception as e:
                                    logger.error(f"点击按钮失败: {e}")
                                return

            elif action == "send_message":
                # 发送消息
                await client(SendMessageRequest(
                    peer=await event.get_input_chat(),
                    message=response
                ))
                logger.info(f"已发送消息: {response}")

            elif action == "send_notification":
                # 发送 PushDeer 通知
                await send_pushdeer_notification("签到提醒", message_text)
                logger.info(f"已发送 PushDeer 通知: {message_text}")
            elif action == "未响音乐服手动签到提醒":
                # 未响音乐服手动签到提醒
                await check_manual_signin_reminder(event,bot_entity, bot_rules)
                
            elif action == "check_expiry":
                # 检查过期时间并发送提醒
                expiry_date = parse_expiry_date(message_text)
                if expiry_date:
                    remaining_days = (expiry_date - datetime.now()).days
                    if remaining_days <= int(notify_days):
                        await send_pushdeer_notification(
                            "过期提醒",
                            f"您的服务将在 {remaining_days} 天后过期，过期时间：{expiry_date.strftime('%Y-%m-%d')}"
                        )
                        logger.info(f"已发送过期提醒: 剩余 {remaining_days} 天")

async def sign_in_for_bot(bot_username, bot_rules, section):
    """
    为指定机器人执行签到
    :param bot_username: 机器人的用户名
    :param bot_rules: 当前机器人的规则列表
    """
    try:
        # 查找签到机器人
        bot_entity = await client.get_entity(bot_username)

        # 检查是否需要发送初始命令
        initial_command = config.get(section, 'INITIAL_COMMAND', fallback=None)
        if initial_command:
            # 发送初始命令
            await client(SendMessageRequest(
                peer=bot_entity,
                message=initial_command
            ))
            logger.info(f"已向 {bot_username} 发送初始命令: {initial_command}")

            # 监听机器人的回复
            @client.on(events.NewMessage(from_users=bot_entity))
            async def handle_message(event):
                await handle_bot_message(event,bot_username, bot_rules)

            # 等待机器人回复
            await asyncio.sleep(10)  # 根据需要调整等待时间
        else:
            # 获取机器人的最后一条消息并处理
            async for message in client.iter_messages(bot_entity, limit=1):
                class MockEvent:
                    def __init__(self, message):
                        self.message = message

                await handle_bot_message(MockEvent(message),bot_username, bot_rules)
                break

    except Exception as e:
        logger.error(f"{bot_username} 签到失败: {e}")
        await send_pushdeer_notification("签到失败", f"{bot_username} 签到失败: {e}")

async def auto_sign_in():
    """
    主函数：自动签到
    """
    try:
        # 连接 Telegram
        await client.connect()
        if not await client.is_user_authorized():
            # 发送登录验证码
            await client.send_code_request(PHONE_NUMBER)
            code = input("请输入收到的验证码: ")
            await client.sign_in(PHONE_NUMBER, code)

        logger.info("登录成功！")

        # 遍历所有签到机器人配置
        for section in config.sections():
            if section.startswith("Bot_"):
                bot_username = config.get(section, 'BOT_USERNAME')
                bot_rules = []

                # 加载机器人的规则
                for key, value in config.items(section):
                    if key.startswith("rule_") and key.endswith("_pattern"):
                        rule_prefix = key[:-8]  # 去掉 "_pattern"
                        rule = {
                            'pattern': value,
                            'action': config.get(section, f"{rule_prefix}_action", fallback=""),
                            'response': config.get(section, f"{rule_prefix}_response", fallback=""),
                            'notify_days': config.get(section, f"{rule_prefix}_notify_days", fallback=None)
                        }
                        bot_rules.append(rule)

                logger.info(f"=========>开始进行机器人: {bot_username} 的签到工作")
                logger.info(f"配置: {bot_rules} ")
                await sign_in_for_bot(bot_username, bot_rules, section)
                logger.info(f"=========>机器人: {bot_username} 的签到工作已经结束")

    except Exception as e:
        logger.error(f"签到失败: {e}")
        await send_pushdeer_notification("签到失败", f"签到失败: {e}")
    finally:
        await client.disconnect()

# 运行脚本
if __name__ == "__main__":
    with client:
        client.loop.run_until_complete(auto_sign_in())
