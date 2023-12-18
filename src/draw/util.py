import textwrap
from io import BytesIO

import aiohttp
from PIL import ImageDraw
from PIL import Image

pic_path = "./src/static/mai/images"


def get_color_code(dx_rating):
    if 0 <= dx_rating <= 999:
        return '00'
    elif 1000 <= dx_rating <= 1999:
        return '01'
    elif 2000 <= dx_rating <= 3999:
        return '02'
    elif 4000 <= dx_rating <= 6999:
        return '03'
    elif 7000 <= dx_rating <= 9999:
        return '04'
    elif 10000 <= dx_rating <= 11999:
        return '05'
    elif 12000 <= dx_rating <= 12999:
        return '06'
    elif 13000 <= dx_rating <= 13999:
        return '07'
    elif 14000 <= dx_rating <= 14499:
        return '08'
    elif 14500 <= dx_rating <= 14999:
        return '09'
    else:
        return '10'


def circle_corner(img, radii=30, border_width=6):
    # 白色区域透明可见，黑色区域不可见
    circle = Image.new('L', (radii * 2, radii * 2), 0)
    draw = ImageDraw.Draw(circle)
    draw.ellipse((0, 0, radii * 2, radii * 2), fill=255)

    img = img.convert("RGBA")
    w, h = img.size

    # 画角
    alpha = Image.new('L', img.size, 255)
    alpha.paste(circle.crop((0, 0, radii, radii)), (0, 0))  # 左上角
    alpha.paste(circle.crop((radii, 0, radii * 2, radii)), (w - radii, 0))  # 右上角
    alpha.paste(circle.crop((radii, radii, radii * 2, radii * 2)), (w - radii, h - radii))  # 右下角
    alpha.paste(circle.crop((0, radii, radii, radii * 2)), (0, h - radii))  # 左下角

    img.putalpha(alpha)

    # Add a black border
    draw = ImageDraw.Draw(img)
    draw.rounded_rectangle(img.getbbox(), outline="black", width=border_width, radius=radii)

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
