import threading
import requests
import time
import os

import botpy

from botpy.logging import DEFAULT_FILE_HANDLER

from src.bot.client import MyClient
from src.utils.app_config import config

from src.database.database_manager import create_tables

if not os.path.exists("local_db.sqlite"):
    create_tables()

if __name__ == "__main__":
    DEFAULT_FILE_HANDLER["filename"] = os.path.join(os.getcwd(), "log", "%(name)s.log")

    intents = botpy.Intents(public_guild_messages=True, direct_message=True, public_messages=True)
    client = MyClient(
        intents=intents,
        is_sandbox=config.bot_config["is_sandbox"],
        timeout=20,
        ext_handlers=DEFAULT_FILE_HANDLER,
    )

    client.run(appid=config.bot_config["appid"], secret=config.bot_config["secret"])
