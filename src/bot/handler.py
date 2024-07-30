"""
handler.py 与 client.py 的区别在于 
handler.py 中的 command_handler 装饰器用于注册命令处理函数
而 client.py 中的 MyClient 类则用于处理命令。
"""

from botpy.message import Message
from botpy import logger, Client
from src.draw.generator import generate_b50
from src.utils.qmsg import send_admin_message
from src.database.database_manager import create_or_update_user_by_id_name
from src.common.alias import get_alias_by_id
from src.common.guess_song import GuessSongHandler

command_handlers = {}


def get_raw_message(message):
    """
    get_raw_message
    """
    logger.debug("get_raw_message: %s", message)
    return message.split(">")[1] if ">" in message else message


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
async def handle_bind_command(self, message: Message):
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
async def handle_b50_command(self, message: Message):
    """
    b50
    """
    logger.debug("%s", self.robot.name)
    message_text = get_raw_message(message.content).replace("/b50", "").strip()
    params = list(message_text)
    _, msg, img = await generate_b50(message.author.id, message.author.avatar, params)
    if img:
        await message.reply(file_image=str(img))
    return msg


@command_handler("/alias")
async def handle_alias_command(self, message: Message):
    """
    alias
    """
    message_text = get_raw_message(message.content).replace("/alias", "").strip()
    if message_text and message_text.isdigit():
        out = await get_alias_by_id(int(message_text))
        if out:
            return f"ID{message_text}的别名有:\n{out}"
        return f"没有找到ID为{message_text}的曲目别名"
    return f"{self.robot.name}:请后面输入曲目的ID查询别名哦"


@command_handler("/曲绘猜歌")
async def handle_guess_command(self: Client, message: Message):
    """
    b50
    """
    logger.debug("%s", self.robot.name)
    get_raw_message(message.content).replace("/曲绘猜歌", "").strip()
    guess_handler = GuessSongHandler(self, message)
    await guess_handler.start_game(message.id)
    return


async def default_handler(self: Client, message: Message):
    """
    default_handler
    """
    guess_handler = GuessSongHandler(self, message)
    await guess_handler.guess_song(get_raw_message(message.content), message.id)

    msg = (
        "帮助文档\n欢迎使用"
        + self.robot.name
        + "\n/bind + 用户名: 绑定水鱼查分器用户名 参数: 水鱼用户名\n"
        "/b50 + 参数: 查询b50分数 参数: n:显示乐曲标题(可选)\n"
        'Tips: 在聊天栏中输入 / 可快速唤起机器人，点击"/b50"可快速完成输入'
    )
    return f"@{message.author.username} {self.robot.name} {msg}"
