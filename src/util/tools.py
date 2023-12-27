"""
Tools
"""
import re
import os
from io import BytesIO
import random
import time

import aiohttp
from PIL import ImageDraw, Image
from src.util.context import context, logger


def get_color_code_from_score(score):
    """
    根据分数获取颜色代码。

    Args:
        score (int): 分数。

    Returns:
        tuple: 颜色代码，格式为 (R, G, B)。
    """
    if score < 1000:
        return 0, 0, 0  # 白色
    elif score < 2000:
        return 0, 221, 238  # 蓝色
    elif score < 4000:
        return 0, 204, 85  # 绿色
    elif score < 7000:
        return 238, 136, 17  # 黄色
    elif score < 10000:
        return 238, 0, 17  # 红色
    elif score < 12000:
        return 238, 0, 238  # 紫色
    elif score < 13000:
        return 136, 51, 0  # 青铜色
    elif score < 14000:
        return 91, 140, 170  # 银色
    elif score < 14500:
        return 255, 195, 0  # 金色
    elif score < 15000:
        return 255, 215, 0  # 白金色
    else:
        # 彩虹渐变效果
        return 0, 0, 0


def get_img_code_from_dx_rating(dx_rating):
    """
    根据 DX 评级获取图片代码。

    Args:
        dx_rating (int): DX 评级。

    Returns:
        str: 图片代码。
    """
    if 0 <= dx_rating <= 999:
        return "00"
    elif 1000 <= dx_rating <= 1999:
        return "01"
    elif 2000 <= dx_rating <= 3999:
        return "02"
    elif 4000 <= dx_rating <= 6999:
        return "03"
    elif 7000 <= dx_rating <= 9999:
        return "04"
    elif 10000 <= dx_rating <= 11999:
        return "05"
    elif 12000 <= dx_rating <= 12999:
        return "06"
    elif 13000 <= dx_rating <= 13999:
        return "07"
    elif 14000 <= dx_rating <= 14499:
        return "08"
    elif 14500 <= dx_rating <= 14999:
        return "09"
    else:
        return "10"


def draw_rainbow_text(img, position, text, font):
    """
    在图片上绘制彩虹渐变文字。

    Args:
        img (PIL.Image.Image): 图片对象。
        position (tuple): 文字位置，格式为 (x, y)。
        text (str): 文字内容。
        font (PIL.ImageFont.FreeTypeFont): 字体对象。
    """
    word = text
    word_position = position
    # 文字区域的box坐标
    word_box = font.getbbox(word)
    # 渐变颜色效果图片
    font_gradient_file_path = os.path.join(
        context["assets_path"], "img", "gradient.png"
    )

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
    # 白色区域透明可见，黑色区域不可见
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


def has_only_common_characters(input_str):
    """
    判断字符串是否只包含常见字符、英文和数字。

    Args:
        input_str (str): 输入字符串。

    Returns:
        bool: 如果字符串只包含常见字符、英文和数字，则返回 True，否则返回 False。
    """
    # 使用正则表达式匹配只含有常见字符、英文和数字的字符串
    pattern = re.compile("^[a-zA-Z0-9!@#$%^&*()-_+=<>?/.,;:'\"\\s]+$")
    return bool(pattern.match(input_str))


def generate_boolean_with_probability(probability):
    """
    根据给定的概率生成布尔值。

    Args:
        probability (int): 期望的概率，范围为1-100。

    Returns:
        bool: 根据概率生成的布尔值。
    """
    # 确保概率在合法范围内
    probability = max(0, min(100, probability))
    # 生成一个在1到100之间的随机数
    random_number = random.randint(1, 100)
    # 如果随机数小于等于概率，返回True；否则返回False
    return random_number <= probability


async def fetch_image(source):
    if source.startswith("http"):
        # 处理云端链接
        async with aiohttp.ClientSession() as session:
            async with session.get(source) as response:
                image_data = await response.read()
                return Image.open(BytesIO(image_data))
    else:
        # 处理本地文件
        with open(source, "rb") as file:
            image_data = file.read()
            return Image.open(BytesIO(image_data))


def time_count():
    """
    计算函数执行时间的装饰器。

    Returns:
        function: 装饰器。
    """

    def decorator(func):
        async def wrapper(*args, **kwargs):
            time_start = time.time()
            result = await func(*args, **kwargs)
            time_end = time.time()
            logger.info(
                f"Function {func.__name__} executed in {time_end - time_start}s"
            )
            return result

        return wrapper

    return decorator


def is_valid_luoxue_username(s):
    # 检查字符串是否为纯数字
    if not s.isdigit():
        return False

    # 检查字符串长度是否在6到10之间
    if 6 < len(s) < 11:
        return True
    else:
        return False
