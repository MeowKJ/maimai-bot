"""
client.py
"""

import botpy
from botpy import logger
from botpy.message import Message, DirectMessage, GroupMessage
from src.database.database_manager import create_tables

from src.bot.handler import command_handlers, default_handler

from src.utils.gpt import chat_history, chat_with_qianfan

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
            await default_handler(self, message)

    async def on_direct_message_create(self, message: DirectMessage):
        """
        on_direct_message_create
        """
        if message.content.startswith("/b50") or message.content.startswith("/bind"):
            await message.reply(
                content=f"{message.author.username}你好! {self.robot.name}暂未开放私聊权限，请在群聊中使用指令❤️"
            )

    async def on_group_at_message_create(self, message: GroupMessage):
        r = chat_with_qianfan(message.content)
        await message.reply(content=f"{r}")
        # message_result = await message._api.post_group_message(
        #     group_openid=message.group_openid,
        #     msg_type=0,
        #     msg_id=message.id,
        #     content=f"收到了消息：{message.content}")
        logger.info("Message result: %s", r)