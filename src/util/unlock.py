import base64

import aiohttp
from cryptography.fernet import Fernet

from src.database.database_manager import (
    get_unlock_id_by_user_id,
    update_unlock_id_by_user_id,
)
from src.util.context import UNLOCK_KEY

cipher_suite = Fernet(UNLOCK_KEY)


async def unlock(user_id):
    """
    Unlocks.
    """
    unlock_id_encrypted = await get_unlock_id_by_user_id(user_id)
    if unlock_id_encrypted is None:
        return "你还没有绑定ID"
    else:
        # 解密用户ID
        unlock_id = cipher_suite.decrypt(base64.b64decode(unlock_id_encrypted)).decode(
            "utf-8"
        )
        print(unlock_id)
        # 构建API请求URL
        api_url = f"https://maihook.lemonkoi.one/api/idunlocker?userid={unlock_id}"

        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    # 读取响应文本
                    result = await response.text()
                    return result
                else:
                    return f"HTTP请求失败，状态码: {response.status}"


async def bind_unlock_id(user_id, unlock_id):
    """
    Binds using Fernet symmetric encryption.
    """
    # 加密 unlock_id
    unlock_id_encrypted = base64.b64encode(
        cipher_suite.encrypt(unlock_id.encode("utf-8"))
    ).decode("utf-8")

    # 更新用户的解锁ID
    await update_unlock_id_by_user_id(user_id, unlock_id_encrypted)

    return "绑定成功"
