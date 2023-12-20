"""
This module provides the DrawingBoard class for creating images.
"""
import os
from PIL import Image, ImageDraw, ImageFont

from src.util.context import context


class DrawingBoard:

    """
    Represents a drawing board for creating images.
    """

    def __init__(
        self,
        main_img_path,
        resize=None,
    ):
        """
        Initializes a DrawingBoard object.

        Args:
        - main_img_path (str): The path to the main image file.
        - resize (tuple, optional): The target size to resize the main image. Defaults to None.
        """
        self.assets_path = context["assets_path"]
        self.font_path = context["font_path"]
        self.en_font = context["en_font"]
        self.jp_font = context["jp_font"]
        self.mix_font = context["mix_font"]
        self.main_img = Image.open(main_img_path)
        self.main_draw = ImageDraw.Draw(self.main_img)
        if resize is not None:
            self.main_img = self.main_img.resize(resize)

    def paste(self, img, position):
        """
        Pastes an image onto the main image at the specified position.

        Args:
        - img (PIL.Image.Image or DrawingBoard): The image to paste.
        - position (tuple): The position coordinates to paste the image.
        """
        if isinstance(img, DrawingBoard):
            self.main_img.paste(img.main_img, position, img.main_img)
        elif isinstance(img, Image.Image):
            self.main_img.paste(img, position, img)
        else:
            raise ValueError(
                "Invalid image type. Expected PIL.Image.Image or DrawingBoard."
            )

    def get_font(self, size, font=context["en_font"]):
        """
        Returns a font object of the specified size.

        Args:
        - size (int): The font size.
        - font (str, optional): The font file name. Default en_font.

        Returns:
        - PIL.ImageFont.FreeTypeFont: The font object.
        """
        return ImageFont.truetype(os.path.join(self.font_path, font), size=size)

    def save(self, path):
        """
        Saves the image to the specified path.

        Args:
        - path (str): The path to save the image.
        """
        self.main_img.save(path)

    def show(self):
        """
        Displays the image.
        """
        self.main_img.show()
