import os
import asyncio

import botpy
from botpy.logging import DEFAULT_FILE_HANDLER

from src.bot.client import MyClient
from src.utils.app_config import config
from src.database.database_manager import create_tables

async def initialize_database():
    if not os.path.exists("local_db.sqlite"):
        await create_tables()

async def main():
    # 设置日志文件路径
    DEFAULT_FILE_HANDLER["filename"] = os.path.join(os.getcwd(), "log", "%(name)s.log")

    # 初始化数据库
    await initialize_database()

    # 设置 bot 的 intents
    intents = botpy.Intents(public_guild_messages=True, direct_message=True, public_messages=True)
    
    # 创建并配置客户端
    client = MyClient(
        intents=intents,
        is_sandbox=config.bot_config["is_sandbox"],
        timeout=20,
        ext_handlers=DEFAULT_FILE_HANDLER,
    )

    # 直接调用 start 方法而不是 run
    await client.start(appid=config.bot_config["appid"], secret=config.bot_config["secret"])

if __name__ == "__main__":
    # 如果你的环境已经在运行一个事件循环（例如 Jupyter Notebook），不要使用 asyncio.run()
    # 直接调用 main()，并通过 loop 运行它
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
