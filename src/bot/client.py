"""
client.py
"""

import botpy
from botpy import logger
from botpy.message import Message, DirectMessage

from src.database.database_manager import create_tables

command_handlers = {}


def get_raw_message(message):
    """
    get_raw_message
    """
    print(message)
    return message.split(">")[1] if ">" in message else message


class MyClient(botpy.Client):
    """
    MyClient
    """

    async def on_ready(self):
        await create_tables()
        logger.info("robot 「%s」 on_ready!", self.robot.name)

    async def on_at_message_create(self, message: Message):
        """
        on_at_message_create
        """
        logger.info("Received message from user: %s", message.author.username)
        logger.info("Message content: %s", message.content)

        for command, handler in command_handlers.items():
            if command in message.content:
                msg = await handler(self, message)
                if msg:
                    await message.reply(
                        content=f"@{message.author.username} {self.robot.name} {msg}"
                    )
                break
        else:
            # 默认帮助信息
            msg = (
                "帮助文档\n欢迎使用"
                + self.robot.name
                + "\n/bind + 用户名: 绑定水鱼查分器用户名 参数: 水鱼用户名\n"
                "/b50 + 参数: 查询b50分数 参数: n:显示乐曲标题(可选)\n"
                'Tips: 在聊天栏中输入 / 可快速唤起机器人，点击"/b50"可快速完成输入'
            )
            await message.reply(
                content=f"@{message.author.username} {self.robot.name} {msg}"
            )

    async def on_direct_message_create(self, message: DirectMessage):
        """
        on_direct_message_create
        """
        if message.content.startswith("/b50") or message.content.startswith("/bind"):
            await message.reply(
                content=f"{message.author.username}你好! {self.robot.name}暂未开放私聊权限，请在群聊中使用指令❤️"
            )
