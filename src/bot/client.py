"""
client.py
"""

import botpy
from botpy import logger
from botpy.message import Message, DirectMessage
from src.database.database_manager import create_tables

from src.bot.handler import command_handlers, default_handler


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
