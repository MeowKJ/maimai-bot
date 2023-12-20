import asyncio
import os
import re
import subprocess
from io import BytesIO

import aiohttp
from PIL import ImageDraw, ImageFont, Image
from botpy import logging

_log = logging.get_logger()

pic_path = "./src/static/mai/images"


def get_color_code2(score):
    if score < 1000:
        return 255, 255, 255  # 白色
    elif score < 2000:
        return 0, 0, 255  # 蓝色
    elif score < 4000:
        return 0, 128, 0  # 绿色
    elif score < 7000:
        return 255, 255, 0  # 黄色
    elif score < 10000:
        return 255, 0, 0  # 红色
    elif score < 12000:
        return 128, 0, 128  # 紫色
    elif score < 13000:
        return 184, 115, 51  # 青铜色
    elif score < 14000:
        return 91, 140, 170  # 银色
    elif score < 14500:
        return 255, 215, 0  # 金色
    elif score < 15000:
        return 255, 195, 0  # 白金色
    else:
        # 彩虹渐变效果
        return 0, 0, 0


def get_color_code(dx_rating):
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


def draw_rainbow_text(img, position, text, font, font_size):
    word = text
    word_position = position
    # 文字区域的box坐标
    word_box = font.getbbox(word)
    # 渐变颜色效果图片
    font_gradient_file_path = "./src/static/mai/img/gradient.png"

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
    async with session.get(avatar_url) as response:
        return await response.read()


async def process_avatar(avatar_url):
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
