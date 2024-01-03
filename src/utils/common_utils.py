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
    try:
        if source.startswith("http"):
            async with aiohttp.ClientSession() as session:
                async with session.get(source) as response:
                    if response.status == 200:
                        image_data = await response.read()
                        return Image.open(BytesIO(image_data))
                    else:
                        raise Exception(
                            f"Unable to fetch image: HTTP {response.status}"
                        )
        else:
            with open(source, "rb") as file:
                image_data = file.read()
                return Image.open(BytesIO(image_data))
    except Exception as e:
        print(f"Error fetching image: {e}")
        return None


def is_valid_luoxue_username(s):
    # 检查字符串是否为纯数字
    if not s.isdigit():
        return False

    # 检查字符串长度是否在6到10之间
    return 6 < len(s) < 11
