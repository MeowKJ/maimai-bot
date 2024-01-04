import time

import aiohttp
from botpy import logger

from .app_config import config


async def send_admin_message(msg: str):
    qmsg_key = config.qmsg_key
    url = f"https://qmsg.zendee.cn/send/{qmsg_key}"
    params = {
        "msg": f"[maimai-bot][项目推送] {msg} \n{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}",
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url, params=params) as resp:
            if resp.status == 200:
                logger.info("Successfully sent message to admin")
                return True
            else:
                logger.error("Failed to send message to admin")
                return False
