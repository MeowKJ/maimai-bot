"""
This module represents a profile drawing board.
"""

from PIL import Image, ImageDraw

from src.draw.drawing_board import DrawingBoard
from src.utils.common_utils import (
    has_only_common_characters,
    get_img_code_from_dx_rating,
)

from src.utils.image_utils import process_avatar, circle_corner

from src.assets_generator.get_assets import AssetType


class ProfileDrawingBoard(DrawingBoard):
    """
    Represents a profile drawing board.
    """

    def __init__(self, main_img_path, rating, name, avatar, name_plate):
        """
        Initialize the ProfileDrawingBoard class.

        Args:
            main_img_path (str): The path to the main image.
            rating (int): The rating of the profile.
            name (str): The name of the profile.
            avatar (image.pyi): The avatar image.
            name_plate (str): The name plate image.
        """
        super().__init__(main_img_path, resize=(1160, 200))
        self.avatar = avatar
        self.name = name
        self.rating = int(rating)
        self.name_plate = name_plate

    async def draw_rating_plate(self, position=(200, 17)):
        """
        Draw the rating plate on the profile drawing board.

        Args:
            position (tuple, optional): The position of the rating plate. Defaults to (200, 17).
        """
        # Get the rating plate image
        rating_plate_img = Image.open(
            self.asstes.generate_assets_path(
                "dx_rating",
                f"UI_CMN_DXRating_S_{get_img_code_from_dx_rating(self.rating)}_waifu2x_2x_png.png",
            )
        )
        rating_plate_img = rating_plate_img.resize((348, 72))
        rating_plate_draw = ImageDraw.Draw(rating_plate_img)
        rating_plate_draw.text(
            (175, 20),
            " ".join(str(self.rating)),
            font=(self.get_font(33)),
            fill=(255, 215, 0),
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            align="center",
        )

        self.paste(rating_plate_img, position)

    async def draw_avatar(self, position=(7, 8)):
        """
        Draw the avatar on the profile drawing board.

        Args:
            position (tuple, optional): The position of the avatar. Defaults to (7, 8).
        """

        if self.avatar:
            if self.avatar.startswith("http"):
                avatar_image = await process_avatar(self.avatar)
            else:
                avatar_path = await self.asstes.get(AssetType.AVATAR, self.avatar)
                avatar_image = Image.open(avatar_path)

            # Convert the image to RGB mode (remove transparency)
            avatar_image = avatar_image.convert("RGBA")

            avatar_image = avatar_image.resize((185, 185))

            # Apply circle corner to the avatar
            avatar_image = circle_corner(avatar_image, radii=15)
            self.paste(avatar_image, position)

    async def draw_name_plate(self, position=(200, 99)):
        """
        Draw the name plate on the profile drawing board.

        Args:
            position (tuple, optional): The position of the name plate. Defaults to (120, 75).
        """
        name_plate_img = Image.open(self.asstes.generate_assets_path("name.png"))
        name_plate_draw = ImageDraw.Draw(name_plate_img)
        name = str(self.name)  # Fix: Replace 'name' with 'self.name'
        # Choose font based on the name content
        if has_only_common_characters(name):
            font = self.get_font(48)
        else:
            font = self.get_font(48, font=self.mix_font)

        name_plate_draw.text((12, 16), name, font=font, fill=(0, 0, 0))

        self.paste(name_plate_img, position)

    async def draw(self):
        """
        Draw the profile drawing board.

        Returns:
            Image: The profile drawing board image.
        """
        await self.draw_rating_plate()
        await self.draw_name_plate()
        await self.draw_avatar()
        return self.main_img
