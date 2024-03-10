"""
图片处理工具。
"""

import asyncio
import os
import subprocess
import aiohttp

from PIL import Image, ImageDraw
from io import BytesIO


def draw_rainbow_text(img, position, text, font, gradient_file):
    """
    在图片上绘制彩虹渐变文字。

    Args:
        img (PIL.Image.Image): 图片对象。
        position (tuple): 文字位置，格式为 (x, y)。
        text (str): 文字内容。
        font (PIL.ImageFont.FreeTypeFont): 字体对象。
        gradient_file (str): 渐变颜色效果图片路径。
    """
    word = text
    word_position = position
    # 文字区域的box坐标
    word_box = font.getbbox(word)
    # 渐变颜色效果图片
    # font_gradient_file_path = os.path.join(
    #     static_config["assets_path"], "img", "gradient.png"
    # )
    font_gradient_file_path = gradient_file
    # 生成文字区域的alpha图片
    font_gradient_im = Image.open(font_gradient_file_path)
    font_gradient_im = font_gradient_im.resize(
        (word_box[2] - word_box[0], word_box[3] - word_box[1])
    )
    font_alpha = Image.new("L", font_gradient_im.size)
    font_alpha_d = ImageDraw.Draw(font_alpha)
    font_alpha_d.text((0, 0), word, fill="White", anchor="lt", font=font)
    font_gradient_im.putalpha(font_alpha)

    img.paste(font_gradient_im, word_position, font_gradient_im)


def circle_corner(img, radii=30, border_width=6):
    """
    将图片的角变为圆角。

    Args:
        img (PIL.Image.Image): 图片对象。
        radii (int): 圆角半径。
        border_width (int): 边框宽度。

    Returns:
        PIL.Image.Image: 处理后的图片对象。
    """
    # 白色区域透明可见，黑色区域不可见、
    circle = Image.new("L", (radii * 2, radii * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)

    img = img.convert("RGBA")
    w, h = img.size

    # 画角
    alpha = Image.new("L", img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(
        circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii)
    )  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角

    img.putalpha(alpha)

    # Add a black border
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(
        img.getbbox(), outline="black", width=border_width, radius=radii
    )

    return img


async def compress_png(fp, output, force=True, quality=None):
    """
    Compresses a PNG file asynchronously.

    Args:
        fp (str): The file path of the original PNG file.
        output (str): The file path for the compressed PNG file.
        force (bool, optional): Whether to force compression. Defaults to True.
        quality (int or str, optional): Compression quality parameter. Defaults to None.

    Returns:
        float: Compression ratio percentage.
    """
    if not os.path.exists(fp):
        raise FileNotFoundError(f"File not found: {fp}")

    force_command = "-f" if force else ""
    quality_command = ""

    if quality and isinstance(quality, int):
        quality_command = f"--quality {quality}"
    if quality and isinstance(quality, str):
        quality_command = f"--quality {quality}"

    command = (
        f"pngquant {fp} "
        f"--skip-if-larger {force_command} "
        f"{quality_command} "
        f"--output {output}"
    )

    try:
        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        _, _ = await process.communicate()

        # 获取原始图像大小
        original_size = os.path.getsize(fp)

        # 获取压缩后文件的大小
        compressed_size = os.path.getsize(output)

        # 计算压缩比
        compression_ratio = (1 - compressed_size / original_size) * 100
        # 检查命令是否成功执行
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)

        return compression_ratio
        # 剩下的代码...
    except asyncio.CancelledError as exc:
        # 处理异步任务被取消的情况
        raise exc from None
    except Exception as e:
        # 处理其他异常
        raise RuntimeError(f"An error occurred: {e}") from e


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
