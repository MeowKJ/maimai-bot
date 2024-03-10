"""
common_utils.py - 通用工具函数。
"""

import random
import re
from io import BytesIO

import aiohttp
from PIL import Image


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
    """
    download image from source

    Args:
        source (str): image url or local file path.

    Returns:
        PIL.Image.Image: image object.
    """
    if source.startswith("http"):
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(source) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        return Image.open(BytesIO(image_data))
        except aiohttp.ClientError as e:
            print(f"An error occurred: {e}")

    else:
        try:
            with open(source, "rb") as file:
                image_data = file.read()
                return Image.open(BytesIO(image_data))
        except FileNotFoundError as e:
            print(f"File not found: {e}")
        except PermissionError as e:
            print(f"Permission denied: {e}")
    return None


def is_valid_luoxue_username(s):
    """
    检查洛雪用户名是否合法。

    Args:
        s (str): 输入的用户名。

    Returns:
        bool: 如果用户名合法，则返回 True, 否则返回 False。
    """
    # 检查字符串是否为纯数字
    if not s.isdigit():
        return False

    # 检查字符串长度是否在6到10之间
    return 6 < len(s) < 11


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
