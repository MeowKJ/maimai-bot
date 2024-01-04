import botpy
from botpy import logger
from botpy.message import Message, DirectMessage

from src.bot.message import get_raw_message
from src.database.database_manager import (
    create_or_update_user_by_id_name,
    create_tables,
)
from src.draw.generator import generate_b50

command_handlers = {}


def command_handler(command):
    def decorator(func):
        command_handlers[command] = func
        return func

    return decorator


class MyClient(botpy.Client):
    async def on_ready(self):
        await create_tables()
        logger.info(f"robot 「{self.robot.name}」 on_ready!")

    @command_handler("/bind")
    async def handle_bind_command(self, message: Message):
        message_text = get_raw_message(message.content).replace("/bind", "").strip()
        if not message_text:
            return f"{self.robot.name}发现你要绑定的用户名是空的"
        if await create_or_update_user_by_id_name(message.author.id, message_text):
            return f"[{message_text}]已经绑定到你的频道号了"
        else:
            return f"绑定[{message_text}]失败，发生了错误"

    @command_handler("/b50")
    async def handle_b50_command(self, message: Message):
        message_text = get_raw_message(message.content).replace("/b50", "").strip()
        params = list(message_text)
        _, msg, img = await generate_b50(
            message.author.id, message.author.avatar, params
        )
        if img:
            await message.reply(file_image=img)
        return msg

    async def on_at_message_create(self, message: Message):
        logger.info(f"Received message from user: {message.author.username}")
        logger.info(f"Message content: {message.content}")

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
                "帮助文档\n欢迎使用" + self.robot.name + "\n/bind + 用户名: 绑定水鱼查分器用户名 参数: 水鱼用户名\n"
                "/b50 + 参数: 查询b50分数 参数: n:显示乐曲标题(可选)\n"
                'Tips: 在聊天栏中输入 / 可快速唤起机器人，点击"/b50"可快速完成输入'
            )
            await message.reply(
                content=f"@{message.author.username} {self.robot.name} {msg}"
            )

    async def on_direct_message_create(self, message: DirectMessage):
        if message.content.startswith("/b50") or message.content.startswith("/bind"):
            await message.reply(
                content=f"{message.author.username}你好! {self.robot.name}目前暂未开放私聊权限，请在群聊中使用"
            )
