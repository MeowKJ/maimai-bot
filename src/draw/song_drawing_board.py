"""
This module contains the SongDrawingBoard class.
"""
import os
import textwrap
from PIL import Image, ImageDraw
from src.draw.drawing_board import DrawingBoard
from src.context import context


class SongDrawingBoard(DrawingBoard):
    """
    Represents a song drawing board.
    """

    def __init__(self, song_data):
        """
        Initialize the SongDrawingBoard object.

        Args:
        - song_data: A dictionary containing song data.

        Attributes:
        - achievement: Song achievement
        - ds: Song difficulty level
        - fc: Song single player badge
        - fs: Song multiplayer badge
        - level_index: Song difficulty index
        - ra: Song rating
        - rate: Song score
        - song_id: Song ID
        - title: Song title
        - _type: Song type
        """
        self.achievement = song_data["achievements"]
        self.ds = song_data["ds"]
        self.fc = song_data["fc"]
        self.fs = song_data["fs"]
        self.level_index = song_data["level_index"]
        self.ra = song_data["ra"]
        self.rate = song_data["rate"]
        self.song_id = song_data["song_id"]
        self.title = song_data["title"]
        self._type = song_data["type"]
        main_img_path = os.path.join(
            context["assets_path"], "song", "base", f"{self.level_index}.png"
        )
        super().__init__(main_img_path, resize=(190, 252))

    def draw_song_cover(self, position=(19, 13)):
        """
        Draw the song cover.

        Args:
        - position: The coordinates for drawing the cover. Default is (19, 13).
        """
        # Format the song ID
        formatted_song_id = str(self.song_id).zfill(5)
        # Get the cover image path
        cover_img_path = os.path.join(
            self.assets_path, "song", "cover", f"{formatted_song_id}.png"
        )
        # Open the cover image
        cover_img = Image.open(cover_img_path)
        # Resize the cover image
        cover_img = cover_img.resize((152, 152))
        # Paste the cover image onto the main image
        self.main_img.paste(cover_img, position, cover_img)

    def draw_song_type(self, position=(6, 3)):
        """
        Draw the song type.

        Args:
        - position: The coordinates for drawing the type. Default is (6, 3).
        """
        type_img_path = os.path.join(
            self.assets_path, "song", f"{self._type.lower()}.png"
        )
        type_img = Image.open(type_img_path)
        type_img = type_img.resize((85, 22))
        self.main_img.paste(type_img, position, type_img)

    def draw_song_rank(self, position=(130, 0), font_size=18):
        """
        Draw the song rank.

        Args:
        - position: The coordinates for drawing the rank. Default is (130, 0).
        - font_size: The font size for the rank. Default is 18.
        """
        ra_plate_img_path = os.path.join(self.assets_path, "song", "ra_base.png")
        ra_plate_img = Image.open(ra_plate_img_path)
        ra_plate_img = ra_plate_img.resize((60, 32))

        font_ra = self.get_font(font_size)
        draw_ra_plate = ImageDraw.Draw(ra_plate_img)
        draw_ra_plate.text(
            (12, 7),
            str(self.ra),
            font=font_ra,
            fill=(255, 200, 0),
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            align="center",
        )
        self.main_img.paste(ra_plate_img, position, ra_plate_img)

    def draw_song_ds(self, position=(12, 7), font_size=19):
        """
        Draw the song difficulty level.

        Args:
        - position: The coordinates for drawing the difficulty level.
        - font_size: The font size for the difficulty level.
        """
        draw_base = ImageDraw.Draw(self.main_img)
        draw_base.text(
            position,
            str(self.ds),
            font=self.get_font(font_size),
            fill=(255, 255, 255),
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            align="center",
        )

    def draw_song_rate(self, position=(10, 210), target_height=32):
        """
        Draw the song score.

        Args:
        - position: The coordinates for drawing the score. Default is (10, 210).
        - target_height: The target height for the score image. Default is 32.
        """
        if self.rate:
            rate_img_path = os.path.join(
                self.assets_path, "song", "rank", f"{self.rate}.png"
            )
            rate_img = Image.open(rate_img_path)
            aspect_ratio = rate_img.width / rate_img.height
            target_width = int(target_height * aspect_ratio)
            rate_img = rate_img.resize((target_width, target_height))
            self.main_img.paste(rate_img, position, rate_img)

    def draw_song_achievement(self, position=(75, 215), font_size=20):
        """
        Draw the song achievement.

        Args:
        - position: The coordinates for drawing the achievement. Default is (75, 215).
        - font_size: The font size for the achievement. Default is 20.
        """
        if self.achievement:
            self.main_draw.text(
                position,
                f"{self.achievement:.4f}",
                font=self.get_font(font_size),
                fill=(255, 255, 255),
                stroke_width=1,
                stroke_fill=(0, 0, 0),
                align="center",
            )

    def draw_song_title(self, position=(20, 25), font_size=16):
        """
        Draw the song title.

        Args:
        - position: The coordinates for drawing the title. Default is (20, 25).
        - font_size: The font size for the title. Default is 16.
        """
        wrapped_text = textwrap.fill(str(self.title), width=11, break_long_words=True)

        self.main_draw.text(
            position,
            wrapped_text,
            font=self.get_font(font_size),
            fill=(255, 255, 255),
            stroke_width=2,
            stroke_fill=(0, 0, 0),
        )

    def draw_song_badge(self, position=(135, 125)):
        """
        Draw the song badges.

        Args:
        - position: The coordinates for drawing the badges. Default is (135, 125).
        """
        if self.fc:
            fc_img_path = os.path.join(
                self.assets_path, "song", "badges", f"{self.fc}_s.png"
            )
            fc_img = Image.open(fc_img_path)
            self.paste(fc_img, position)
            position[0] -= 35

        if self.fs:
            fs_img_path = os.path.join(
                self.assets_path, "song", "badges", f"{self.fs}_s.png"
            )
            fs_img = Image.open(fs_img_path)
            self.paste(fs_img, position)

    def draw(self, is_draw_title=False):
        """
        Draw the song card.

        Args:
        - is_draw_title: Whether to draw the song title. Default is False.
        """

        # Draw the song cover
        self.draw_song_cover()

        # Draw the song type
        self.draw_song_type()

        # Draw the song rank
        self.draw_song_rank()

        # Draw the song difficulty level
        self.draw_song_ds()

        # Draw the song rating
        self.draw_song_rate()

        # Draw the song achievement
        self.draw_song_achievement()

        if is_draw_title:
            # Draw the song title
            self.draw_song_title()

        # Draw the song badges
        self.draw_song_badge()

        return self.main_img
