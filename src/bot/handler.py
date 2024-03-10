"""
handler.py 与 client.py 的区别在于 
handler.py 中的 command_handler 装饰器用于注册命令处理函数
而 client.py 中的 MyClient 类则用于处理命令。
"""

from botpy.message import Message
from src.draw.generator import generate_b50
from src.utils.qmsg import send_admin_message
from src.database.database_manager import create_or_update_user_by_id_name

from src.bot.client import get_raw_message, MyClient, command_handlers


def command_handler(command):
    """
    command_handler
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                exception_info = f"Error in {func.__name__}: {str(e)}"
                await send_admin_message(exception_info)
                raise e

        command_handlers[command] = wrapper
        return wrapper

    return decorator


@command_handler("/bind")
async def handle_bind_command(self: MyClient, message: Message):
    """
    bind
    """
    message_text = get_raw_message(message.content).replace("/bind", "").strip()
    if not message_text:
        return f"{self.robot.name}发现你要绑定的用户名是空的"
    if await create_or_update_user_by_id_name(message.author.id, message_text):
        return f"[{message_text}]已经绑定到你的频道号了"
    else:
        return f"绑定[{message_text}]失败，发生了错误"


@command_handler("/b50")
async def handle_b50_command(self: MyClient, message: Message):
    """
    b50
    """
    message_text = get_raw_message(message.content).replace("/b50", "").strip()
    params = list(message_text)
    _, msg, img = await generate_b50(message.author.id, message.author.avatar, params)
    if img:
        await message.reply(file_image=img)
    return f"[{self.robot.name}]" + msg
