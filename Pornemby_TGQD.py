from telethon import TelegramClient

# 请记住使用来自 my.telegram.org 的您自己的值！
api_id = 5672799	#输入api_id，一个账号一项
api_hash = 'e08529171140eac69071c630f03f1a7a'	#输入api_hash，一个账号一项
client = TelegramClient('anon', api_id, api_hash)

async def main():
    # 获取有关您自己的信息
    me = await client.get_me()

    # “我”是一个用户对象。 你可以漂亮地打印
    # 任何带有“stringify”方法的 Telegram 对象：
    print(me.stringify())

    # 当你打印一些东西时，你会看到它的表示。
     # 你可以访问 Telegram 对象的所有属性
     # 点运算符。 例如，要获取用户名：
    username = me.username
    print(username)
    print(me.phone)

    # 您可以打印您参与的所有对话/对话：
    #async for dialog in client.iter_dialogs():
    #    print(dialog.name, 'has ID', dialog.id)

    # 你可以给自己发消息...
    #await client.send_message('me', 'Hello, myself!')
    # ...到某个聊天 ID
    await client.send_message(1849549411, 'Hello, group!')
    # ...给您的联系人
    #await client.send_message('+34600123123', 'Hello, friend!')
    # ...甚至是任何用户名
    await client.send_message('转存-小六花', 'Testing Telethon!')

    # 当然，您可以在消息中使用降价：
    message = await client.send_message(
        'me',
        'This message has **bold**, `code`, __italics__ and '
        'a [nice website](https://example.com)!',
        link_preview=False
    )

    # 发送消息返回已发送的消息对象，您可以使用该对象
    print(message.raw_text)

    # 如果您有消息对象，您可以直接回复消息
    await message.reply('Cool!')

    # 或发送文件、歌曲、文档、专辑...
    await client.send_file('me', '/home/me/Pictures/holidays.jpg')

    # 您可以打印任何聊天的消息历史记录：
    async for message in client.iter_messages('me'):
        print(message.id, message.text)

        # 您也可以从消息中下载媒体！
        # 该方法将返回文件保存的路径。
        if message.photo:
            path = await message.download_media()
            print('File saved to', path)  # 下载完成后打印

with client:
    client.loop.run_until_complete(main())
