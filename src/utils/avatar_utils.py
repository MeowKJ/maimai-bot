"""
头像图片处理工具。
"""

from io import BytesIO

import aiohttp
from PIL import Image

from .image_utils import circle_corner


async def download_avatar(session, avatar_url):
    """
    下载头像图片。

    Args:
        session (aiohttp.ClientSession): Aiohttp 客户端会话对象。
        avatar_url (str): 头像图片的 URL。

    Returns:
        bytes: 下载的头像图片数据。
    """
    async with session.get(avatar_url) as response:
        return await response.read()


async def process_avatar(avatar_url):
    """
    处理头像图片。

    Args:
        avatar_url (str): 头像图片的 URL。

    Returns:
        PIL.Image.Image: 处理后的头像图片对象。
    """
    async with aiohttp.ClientSession() as session:
        avatar_data = await download_avatar(session, avatar_url)

    # Open the avatar image using PIL
    avatar_image = Image.open(BytesIO(avatar_data))

    # Convert the image to RGB mode (remove transparency)
    avatar_image = avatar_image.convert("RGBA")

    avatar_image = avatar_image.resize((185, 185))

    # Apply circle corner to the avatar
    avatar_image = circle_corner(avatar_image, radii=15)
    return avatar_image
