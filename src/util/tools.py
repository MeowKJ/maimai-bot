"""
Tools
"""
import os
import random
import re
import time
from io import BytesIO

import aiohttp
from PIL import ImageDraw, Image

from src.util.context import static_config, logger


def get_color_code_from_score(score):
    """
    根据分数获取颜色代码。

    Args:
        score (int): 分数。

    Returns:
        tuple: 颜色代码，格式为 (R, G, B)。
    """
    score_ranges = [
        (0, 999, (0, 0, 0)),  # 白色
        (1000, 1999, (0, 221, 238)),  # 蓝色
        (2000, 3999, (0, 204, 85)),  # 绿色
        (4000, 6999, (238, 136, 17)),  # 黄色
        (7000, 9999, (238, 0, 17)),  # 红色
        (10000, 11999, (238, 0, 238)),  # 紫色
        (12000, 12999, (136, 51, 0)),  # 青铜色
        (13000, 13999, (91, 140, 170)),  # 银色
        (14000, 14499, (255, 207, 51)),  # 金色
        (14500, 14999, (255, 251, 85)),  # 白金色
    ]
    
    for lower, upper, color in score_ranges:
        if lower <= score <= upper:
            return color
    
    # 彩虹渐变效果，假定为黑色
    return 0, 0, 0


def get_img_code_from_dx_rating(dx_rating):
    """
    根据 DX 评级获取图片代码。

    Args:
        dx_rating (int): DX 评级。

    Returns:
        str: 图片代码。
    """
    ranges = [
        (0, 999, "01"),
        (1000, 1999, "02"),
        (2000, 3999, "03"),
        (4000, 6999, "04"),
        (7000, 9999, "05"),
        (10000, 11999, "06"),
        (12000, 12999, "07"),
        (13000, 13999, "08"),
        (14000, 14499, "09"),
        (14500, 14999, "09"),
    ]

    for lower, upper, code in ranges:
        if lower <= dx_rating <= upper:
            return code

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
        static_config["assets_path"], "img", "gradient.png"
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
    return 6 < len(s) < 11
