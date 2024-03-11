"""
A module for drawing the Maimai game board.
"""

import random
from datetime import datetime
from pathlib import Path
from PIL import Image, ImageDraw

from src.draw.drawing_board import DrawingBoard
from src.draw.profile_drawing_board import ProfileDrawingBoard
from src.draw.song_drawing_board import SongDrawingBoard
from src.utils.common_utils import get_color_code_from_score
from src.utils.image_utils import draw_rainbow_text
from src.assets_generator.get_assets import AssetType

from .data_models.player import Player


class MaimaiDrawingBoard(DrawingBoard):
    """
    A class representing a drawing board for the Maimai game.
    """

    def __init__(
        self,
        main_img_path,
        player: Player,
        is_draw_title=True,
        is_compress_img=True,
    ):
        """
        Initialize an instance of the MaimaiDrawingBoard class.

        Args:
            main_img_path (str): The path of the main image.
            player (Player): The player data.
            is_draw_title (bool, optional): Whether to draw the title. Defaults to False.
            is_compress_img (bool, optional): Whether to compress the image. Defaults to True.
        """
        super().__init__(main_img_path=main_img_path)
        self.player = player

        self.is_draw_title = is_draw_title
        self.is_compress_img = is_compress_img

    async def draw_songs(
        self, is_b15, position_b15=(100, 2050), position_b35=(100, 405)
    ):
        """
        Draw song information on the main image.

        Args:
            is_b15 (bool): Flag indicating whether the songs are B15 or B35.
            position_b15 (tuple, optional): The starting position to draw B15 songs.
                Defaults to (100, 2050).
            position_b35 (tuple, optional): The starting position to draw B35 songs.
                Defaults to (100, 405).
        """
        if is_b15:
            song_data_list = self.player.song_data_b15
            position = position_b15
            position_x = position_b15[0]
            position_y = position_b15[1]
        else:
            song_data_list = self.player.song_data_b35
            position = position_b35
            position_x = position_b35[0]
            position_y = position_b35[1]
        x, y = 0, 0
        for song_data in song_data_list:
            base_color = ""
            if song_data.achievements >= 100:
                base_color = "_r"
            elif song_data.achievements >= 99:
                base_color = "_g"

            main_img_path = self.asstes.generate_assets_path(
                "base", f"{song_data.level_index}{base_color}.png"
            )

            song_plate = SongDrawingBoard(main_img_path, song_data, self.is_draw_title)
            await song_plate.draw()
            self.paste(song_plate, (position_x, position_y))
            x = x + 1
            position_x = position_x + 203
            if x == 6:
                y = y + 1
                position_x = position[0]
                position_y = position_y + 267
                x = 0

    def draw_rocket_decor(self, position=(1192, 2643)):
        """
        Draw the main character on the main image.

        Args:
            position (tuple, optional): The starting position to draw the rocket.
                Defaults to (1192, 2643).
        """
        # Implement the content of the draw_character method
        # Draw the rocket
        image_path = self.asstes.generate_assets_path("characters", "rocket_small.png")
        character_img = Image.open(image_path)
        self.main_img.paste(character_img, position, character_img)

    def draw_badge(self, position=(1145, 1725)):
        """
        Draw the badge on the main image.

        Args:
            position (tuple, optional): The starting position to draw the badge.
                Defaults to (1145, 1725).
        """
        # Implement the content of the draw_secondary_character method
        random_number = random.randint(0, 16)
        image_path = self.asstes.generate_assets_path(
            "characters", f"yj{random_number}.png"
        )
        character_img = Image.open(image_path)

        self.main_img.paste(character_img, position, character_img)

    async def draw_profile_plate(
        self, rating, name, avatar, name_plate, position=(120, 75)
    ):
        """
        Draw a plate containing user information on the main image.

        Args:
            rating (int): The user's rating.
            name (str): The username.
            avatar (str): The user's avatar.
            name_plate (str): The name plate image.
            position (tuple, optional): The starting position to draw the profile plate.
                Defaults to (120, 75).
        """
        # Implement the content of the draw_plate method

        if isinstance(self.player.name_plate, int):
            plate_filepath = await self.asstes.get(
                AssetType.PLATE, self.player.name_plate
            )
        else:
            plate_file_list = [
                x for x in Path(self.asstes.assets_folder, "plate").glob("*.png")
            ]
            if len(plate_file_list) > 10:
                plate_filepath = str(random.choice(plate_file_list))
            else:
                plate_filepath = await self.asstes.get(AssetType.PLATE, 0)

        profile_plate = ProfileDrawingBoard(
            plate_filepath,
            rating,
            name,
            avatar,
            name_plate,
        )
        await profile_plate.draw()
        self.paste(profile_plate, position)

    def draw_score_nv(self, b15_scores, b35_scores, position=(315, 290)):
        """
        Draw B15 and B35 score information on the main image.

        Args:
            b15_scores (int): The B15 score.
            b35_scores (int): The B35 score.
            position (tuple, optional): The starting position to draw the scores.
                Defaults to (315, 290).
        """
        x = 130
        y = 35
        b15_scores_q = int(b15_scores * 50 / 15)
        b35_scores_q = int(b35_scores * 50 / 35)
        font_size = 36

        # Create a blank image for drawing
        nv_img = Image.open(self.asstes.generate_assets_path("title_base.png"))
        draw_f = ImageDraw.Draw(nv_img)

        # Add rainbow effect for scores greater than 15000
        if b15_scores_q > 15000:
            draw_rainbow_text(
                nv_img,
                (x, y),
                f"B15 -> {b15_scores}",
                self.get_font(font_size),
                self.asstes.generate_assets_path("gradient.png"),
            )
        else:
            draw_f.text(
                (x, y),
                f"B15 -> {b15_scores}",
                font=self.get_font(font_size),
                fill=get_color_code_from_score(b15_scores_q),
                stroke_width=2,
                stroke_fill=(0, 0, 0),
            )

        if b35_scores_q > 15000:
            draw_rainbow_text(
                nv_img,
                (x + 270, y),
                f"B35 -> {b35_scores}",
                self.get_font(font_size),
                self.asstes.generate_assets_path("gradient.png"),
            )
        else:
            draw_f.text(
                (x + 270, y),
                f"B35 -> {b35_scores}",
                font=self.get_font(font_size),
                fill=get_color_code_from_score(b15_scores_q),
                stroke_width=2,
                stroke_fill=(0, 0, 0),
            )

        self.main_img.paste(nv_img, position, nv_img)

    def draw_footer(self, position=(750, 2600)):
        """
        Draw a footer containing song information on the main image.
        """
        # Implement the content of the draw_footer method
        # Draw the footer
        footer_img_list = ["UI_footer1.png", "UI_footer2.png", "UI_footer3.png"]
        footer_img_name = random.choice(footer_img_list)
        footer_img = Image.open(self.asstes.generate_assets_path(footer_img_name))
        draw_f = ImageDraw.Draw(footer_img)
        font = self.get_font(30)

        if footer_img_name == "UI_footer2.png":
            x = 60
            y = 100
        elif footer_img_name == "UI_footer3.png":
            x = 65
            y = 75
        else:
            y = 75
            x = 40
        if self.player.song_data_b15_total > 0:
            b15_max = self.player.song_data_b15[0].rating
            b15_min = self.player.song_data_b15[-1].rating

            draw_f.text(
                (x, y), f"B15 -> MAX {b15_max} MIN {b15_min}", font=font, fill=(0, 0, 0)
            )

        if self.player.song_data_b35_total > 0:
            b35_max = self.player.song_data_b35[0].rating
            b35_min = self.player.song_data_b35[-1].rating
            draw_f.text(
                (x, y := y + 50),
                f"B35 -> MAX {b35_max} MIN {b35_min}",
                font=font,
                fill=(0, 0, 0),
            )

        font = self.get_font(20, "zh_yuan.otf")
        current_time = datetime.now()

        # Format the time as "xx/xx/xx"
        formatted_time = current_time.strftime("%Y/%m/%d")
        draw_f.text(
            (x, y := y + 50),
            f"更多信息:b50.mpas.top/{self.player.username}",
            font=font,
            fill=(0, 0, 0),
        )
        font = self.get_font(20, "zh_yuan.otf")
        draw_f.text(
            (x, y + 30),
            f"Maimai的频道Bot {formatted_time}",
            font=font,
            fill=(0, 0, 0),
        )

        self.paste(footer_img, position)

    async def draw(self):
        """
        Draw the complete image.
        """
        await self.draw_profile_plate(
            self.player.rating,
            self.player.nickname,
            self.player.avatar_url,
            self.player.name_plate,
        )
        await self.draw_songs(True)
        await self.draw_songs(False)
        self.draw_badge()
        self.draw_score_nv(
            self.player.song_data_b15_total, self.player.song_data_b35_total
        )

        # keep draw_footer before draw_rocket_decor
        self.draw_footer()
        self.draw_rocket_decor()

        return self.main_img
