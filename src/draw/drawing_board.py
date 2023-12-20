import os
from PIL import Image, ImageDraw, ImageFont

from src.context import context



class DrawingBoard:
    def __init__(self, 
                main_img_path,  # 主图像文件的路径。
                resize=None,  # 可选。要调整主图像大小的目标尺寸。默认为None。
                assets_path=context["assets_path"],  # 资源目录的路径。默认为上下文中的值。
                font_path=context["font_path"],  # 字体目录的路径。默认为上下文中的值。
                en_font=context["en_font"],  # 英文文本的字体文件。默认为上下文中的值。
                jp_font=context["jp_font"],  # 日文文本的字体文件。默认为上下文中的值。
                mix_font=context["mix_font"]  # 混合文本的字体文件。默认为上下文中的值。
                ):
        """
        初始化一个DrawingBoard对象。

        Args:
        - main_img_path (str): 主图像文件的路径。
        - resize (tuple, optional): 要调整主图像大小的目标尺寸。默认为None。
        - assets_path (str): 资源目录的路径。默认为上下文中的值。
        - font_path (str): 字体目录的路径。默认为上下文中的值。
        - en_font (str): 英文文本的字体文件。默认为上下文中的值。
        - jp_font (str): 日文文本的字体文件。默认为上下文中的值。
        - mix_font (str): 混合文本的字体文件。默认为上下文中的值。
        """      
        self.assets_path = assets_path
        self.font_path = font_path
        self.en_font = en_font
        self.jp_font = jp_font
        self.mix_font = mix_font
        self.main_img = Image.open(main_img_path)
        self.main_draw = ImageDraw.Draw(self.main_img)
        if resize is not None:
            self.main_img = self.main_img.resize(resize)

    def paste(self, img, position):
        """
        将图像粘贴到主图像上的指定位置。

        Args:
        - img (PIL.Image.Image or DrawingBoard): 要粘贴的图像。
        - position (tuple): 粘贴的位置坐标。
        """
        if isinstance(img, DrawingBoard):
            self.main_img.paste(img.main_img, position)
        elif isinstance(img, Image.Image):
            self.main_img.paste(img, position)
        else:
            raise ValueError("Invalid image type. Expected PIL.Image.Image or DrawingBoard.")
        
        
    def get_font(self, size, font=context["en_font"]):
        """
        获取指定大小的字体对象。

        Args:
        - size (int): 字体大小。
        - font (str, optional): 字体文件名。默认为上下文中的英文字体文件。

        Returns:
        - PIL.ImageFont.FreeTypeFont: 字体对象。
        """
        return ImageFont.truetype(os.path.join(self.font_path, font), size=size)

