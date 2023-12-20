import os

import botpy
from botpy.ext.cog_yaml import read
from botpy.message import Message

from src.draw.db import update_or_insert_user
from src.draw.generater import generate50
from src.util import _log

test_config = read(os.path.join(os.path.dirname(__file__), "config.yaml"))


class MyClient(botpy.Client):
    async def on_ready(self):
        _log.info(f"robot 「{self.robot.name}」 on_ready!")  

    async def on_at_message_create(self, message: Message):

        _log.info(message.author.username)
        _log.info(message.content)

        reply_message = ""
        if "/bind" in message.content:
            message_text = message.content.split(">")[1]
            message_text = message_text.replace("/bind", "")
            message_text = message_text.replace(" ", "")
            if not message_text:
                reply_message = f"{self.robot.name}发现你要绑定的用户名是空的"
            else:
                update_or_insert_user(message.author.id, message_text)
                reply_message = f"[{message_text}]已经绑定到你的频道号了"
        elif "/b50" in message.content:
            message_text = message.content.split(">")[1]
            message_text = message_text.replace("/b50", "")
            message_text = message_text.replace(" ", "")
            params = list(message_text)
            try:
                img, code = await generate50(message.author.id, message.author.avatar, params)
            except Exception as e:
                _log.error(e)
                reply_message = f"{self.robot.name}发现你的b50查询出现了一些问题"
            else:
                if img:
                    if isinstance(img, tuple):
                        img_path, time = img
                        if code == 201:
                            reply_message = f"{self.robot.name}发现你的b50分数距离上次查询没有变化"
                            await message.reply(file_image=img_path)
                        elif code == 200:
                            reply_message = f"{self.robot.name}为你生成了新的b50分数图, 耗时{time:.2f}s"
                            await message.reply(file_image=img_path)
                    else:
                        reply_message = f"{self.robot.name}发现{img}"
        else:
            message_text = message.content.split(">")[1]
            message_text = message_text.replace(" ", "")
            if not message_text:
                msg = (
                    f"帮助文档\n欢迎使用{self.robot.name}\n/bind + 用户名: 绑定水鱼查分器用户名 参数: 水鱼用户名\n/b50 + 参数: 查询b50分数 参数: n:显示乐曲标题("
                    f"可选)\nTips: 在聊天栏中输入 / 可快速唤起机器人，点击\"/b50\"可快速完成输入")
                reply_message = msg

        if reply_message:
            await message.reply(content=f"@{message.author.username} {reply_message}")


if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True)
    client = MyClient(intents=intents)
    client.run(appid=test_config["appid"], secret=test_config["secret"])
