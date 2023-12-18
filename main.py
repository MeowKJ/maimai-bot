import asyncio
import os

import botpy
from botpy import logging
from botpy.ext.cog_yaml import read
from botpy.message import Message

from src.draw.db import update_or_insert_user
from src.draw.generater import generate50

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))

_log = logging.get_logger()


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_at_message_create(self, message: Message):
        _log.info(message.author.avatar)
        _log.info(message.author.username)
        if "/bind" in message.content:
            message_text = message.content.split(">")[1]
            message_text = message_text.replace("/bind", "")
            message_text = message_text.replace(" ", "")
            if not message_text:
                await message.reply(content=f"机器人{self.robot.name}发现你要绑定的用户名是空的")
                return
            update_or_insert_user(message.author.id, message_text)
            await message.reply(
                content=f"[{message_text}]已经绑定到你的频道号了，以后只需要发送/b50就可以就可以生成b50成绩图了")

        if "/b50" in message.content:
            message_text = message.content.split(">")[1]
            message_text = message_text.replace("/b50", "")
            message_text = message_text.replace(" ", "")
            params = list(message_text)
            try:
                img, code = await generate50(message.author.id, message.author.avatar, params)
            except Exception as e:
                _log.error(e)
                await message.reply(content=f"机器人{self.robot.name}发现你的b50查询出现了一些问题")
                return
            if img:
                if code == 200 or code == 201:
                    if code == 201:
                        await message.reply(content=f"机器人{self.robot.name}发现你的b50分数距离上次查询没有变化")
                    await message.reply(file_image=img)
                else:
                    await message.reply(content=img)


if __name__ == "__main__":
    # 通过预设置的类型，设置需要监听的事件通道
    # intents = botpy.Intents.none()
    # intents.public_guild_messages=True

    # 通过kwargs，设置需要监听的事件通道
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
