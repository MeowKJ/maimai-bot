import os
from PIL import Image, ImageDraw

from src.draw.drawing_board import DrawingBoard
from src.util import get_color_code, process_avatar, has_only_common_characters

class ProfileDrawingBoard(DrawingBoard):
    def __init__(self, main_img_path, avatar, name, rating):
        """
        Initialize the ProfileDrawingBoard class.

        Args:
            main_img_path (str): The path to the main image.
            avatar (str): The avatar image.
            name (str): The name of the profile.
            rating (int): The rating of the profile.
        """
        super().__init__(self, main_img_path, resize=(1160, 200))
        self.avatar = avatar
        self.name = name
        self.rating = rating
        
    def draw_rating_palte(self, position=(200, 17)):
        """
        Draw the rating plate on the profile drawing board.

        Args:
            position (tuple, optional): The position of the rating plate. Defaults to (200, 17).
        """
        # Get the rating plate image
        rating_plate_img = Image.open(
            os.path.join(self.assets_path, "dx_rating",
                         f"UI_CMN_DXRating_S_{get_color_code(self.rating)}_waifu2x_2x_png.png")
        )
        rating_plate_img = rating_plate_img.resize((348, 72))
        rating_plate_draw = ImageDraw.Draw(rating_plate_img)
        rating_plate_draw.text((175, 20), " ".join(str(self.rating)), font=self.get_font(34), fill=(255, 215, 0), stroke_width=2,
                           stroke_fill=(0, 0, 0), align='center')
        
        self.paste(rating_plate_img, position)
        
    async def draw_avatar(self, position=(7, 8)):
        """
        Draw the avatar on the profile drawing board.

        Args:
            position (tuple, optional): The position of the avatar. Defaults to (7, 8).
        """
        if self.avatar:
            avatar_pic = await process_avatar(self.avatar)
            self.paste(avatar_pic, position)
        
    def draw_name_plate(self, position=(120, 75)):
        """
        Draw the name plate on the profile drawing board.

        Args:
            position (tuple, optional): The position of the name plate. Defaults to (120, 75).
        """
        name_plate_img = Image.open(os.path.join(self.assets_path, "img", "name.png"))
        name_plate_draw = ImageDraw.Draw(name_plate_img)
        name = str(name)
        # Choose font based on the name content
        if has_only_common_characters(name):
            font = self.get_font(48)
        else:
            font = self.get_font(48, font=self.mix_font)

        name_plate_draw.text((12, 16), name, font=font, fill=(0, 0, 0))

        self.paste(name_plate_img, position)
    
    def draw(self):
        """
        Draw the profile drawing board.
        
        Returns:
            Image: The profile drawing board image.
        """
        self.draw_rating_palte()
        self.draw_name_plate()
        self.draw_avatar()
        return self.main_img