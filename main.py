import threading
import requests
import time
import os

import botpy

from botpy.logging import DEFAULT_FILE_HANDLER

from src.bot.client import MyClient
from src.utils.app_config import config


def heartbeat_request(url):
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            print("Heartbeat request successful!")
        else:
            print("Heartbeat request failed.")
        time.sleep(60)  # 每分钟执行一次请求


if __name__ == "__main__":
    DEFAULT_FILE_HANDLER["filename"] = os.path.join(os.getcwd(), "log", "%(name)s.log")

    intents = botpy.Intents(public_guild_messages=True, direct_message=True)
    client = MyClient(
        intents=intents,
        is_sandbox=config.bot_config["is_sandbox"],
        timeout=20,
        ext_handlers=DEFAULT_FILE_HANDLER,
    )

    # 创建线程并启动
    heartbeat_thread = threading.Thread(
        target=heartbeat_request, args=(config.heartbeat_url,)
    )
    heartbeat_thread.start()

    client.run(appid=config.bot_config["appid"], secret=config.bot_config["secret"])
