"""
This module is the main entry point for the maimai-bot application.
"""
import botpy
from botpy.message import Message, DirectMessage

from src.database.database_manager import (
    create_or_update_user_by_id_name,
    create_tables,
)
from src.draw.generator import generate_b50
from src.util.context import logger
from src.util.unlock import unlock, bind_unlock_id


class MyClient(botpy.Client):
    """
    MyClient is a custom client class that extends the botpy.Client class.
    """

    async def on_ready(self):
        await create_tables()
        logger.info(f"robot 「{self.robot.name}」 on_ready!")

    async def on_direct_message_create(self, message: DirectMessage):
        if message.content.startswith("/bindid"):
            unlock_id = message.content.replace("/bindid", "")
            await bind_unlock_id(message.author.id, unlock_id)
            await message.reply(content="绑定成功")

        if message.content.startswith("o"):
            result = await unlock(message.author.id)
            await message.reply(content=result)

    async def on_at_message_create(self, message: Message):
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
                if await create_or_update_user_by_id_name(
                    message.author.id, message_text
                ):
                    msg = f"[{message_text}]已经绑定到你的频道号了"
                else:
                    msg = f"绑定[{message_text}]失败，发生了错误"
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
