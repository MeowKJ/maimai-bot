"""
This module provides the DrawingBoard class for creating images.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from src.utils.app_config import config
from src.assets_generator.get_assets import Assets


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
        self.asstes = Assets.get_instance()
        self.font_path = config.static_config["font_path"]
        self.en_font = config.static_config["en_font"]
        self.jp_font = config.static_config["jp_font"]
        self.mix_font = config.static_config["mix_font"]
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

    def get_font(self, size, font=config.static_config["en_font"]):
        """
        Returns a font object of the specified size.

        Args:
        - size (int): The font size.
        - font (str, optional): The font file name. Default en_font.

        Returns:
        - PIL.ImageFont.FreeTypeFont: The font object.
        """
        return ImageFont.truetype(str(Path(self.font_path, font)), size=size)

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
