"""
图片处理工具。
"""
from PIL import Image, ImageDraw


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
