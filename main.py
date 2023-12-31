"""
This module is the main entry point for the maimai-bot application.
"""
import os

import botpy
from botpy.logging import DEFAULT_FILE_HANDLER

from src.bot.client import MyClient
from src.util.context import bot_config

DEFAULT_FILE_HANDLER["filename"] = os.path.join(os.getcwd(), "log", "%(name)s.log")


if __name__ == "__main__":
    intents = botpy.Intents(public_guild_messages=True, direct_message=True)
    client = MyClient(
        intents=intents,
        is_sandbox=bot_config["is_sandbox"],
        timeout=20,
        ext_handlers=DEFAULT_FILE_HANDLER,
    )
    client.run(appid=bot_config["appid"], secret=bot_config["secret"])
