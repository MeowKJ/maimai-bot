"""
This module is the main entry point for the maimai-bot application.
"""
import botpy
from botpy.message import Message, DirectMessage

from src.util.database import update_or_insert_user
from src.util.context import logger, app_config
from src.draw import generate_b50
from src.util.unlock import unlock, bind_unlock_id


class MyClient(botpy.Client):
    """
    MyClient is a custom client class that extends the botpy.Client class.
    """

    async def on_ready(self):
        """
        处理机器人准备就绪事件的方法。

        Returns:
            None
        """
        logger.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_direct_message_create(self, message: DirectMessage):
        if message.content.startswith("/bindid"):
            unlock_id = message.content.replace("/bindid", "")
            bind_unlock_id(message.author.id, unlock_id)
            await message.reply(content="绑定成功")

        if message.content.startswith("o"):
            result = await unlock(message.author.id)
            await message.reply(content=result)

    async def on_at_message_create(self, message: Message):
        """
        处理@消息创建事件的方法。

        Args:
            message (Message): 收到的消息对象

        Returns:
            None
        """
        logger.info(f"Received message from user: {message.author.username}")
        logger.info(f"Message content: {message.content}")
        msg = ""
        if "/bind" in message.content:
            message_text = message.content.split(">")[1]
            message_text = message_text.replace("/bind", "")
            message_text = message_text.replace(" ", "")
            if not message_text:
                msg = f"{self.robot.name}发现你要绑定的用户名是空的"
            else:
                update_or_insert_user(message.author.id, message_text)
                msg = f"[{message_text}]已经绑定到你的频道号了"
        elif "/b50" in message.content:
            message_text = message.content.split(">")[1]
            message_text = message_text.replace("/b50", "")
            message_text = message_text.replace(" ", "")
            params = list(message_text)
            _, msg, img = await generate_b50(
                message.author.id, message.author.avatar, params
            )
            if img:
                await message.reply(file_image=img)

        else:
            message_text = message.content.split(">")[1]
            message_text = message_text.replace(" ", "")
            if not message_text:
                msg = (
                    "帮助文档\n欢迎使用"
                    + self.robot.name
                    + "\n/bind + 用户名: 绑定水鱼查分器用户名 参数: 水鱼用户名\n"
                    "/b50 + 参数: 查询b50分数 参数: n:显示乐曲标题(可选)\n"
                    'Tips: 在聊天栏中输入 / 可快速唤起机器人，点击"/b50"可快速完成输入'
                )

        if msg:
            await message.reply(
                content=f"@{message.author.username} {self.robot.name} {msg}"
            )


if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True, direct_message=True)
    client = MyClient(intents=intents, is_sandbox=True, timeout=10)
    client.run(appid=app_config["appid"], secret=app_config["secret"])
