"""
This module contains the SongDrawingBoard class.
"""

import textwrap

from PIL import Image, ImageDraw
from src.assets_generator.get_assets import AssetType

from src.draw.drawing_board import DrawingBoard
from .data_models.song import SongData


class SongDrawingBoard(DrawingBoard):
    """
    Represents a song drawing board.
    """

    def __init__(self, main_img_path, song_data: SongData, is_draw_title):
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
        self.song_data = song_data
        self.is_draw_title = is_draw_title

        super().__init__(main_img_path, resize=(190, 252))

    async def draw_song_cover(self, position=(19, 13)):
        """
        Draw the song cover.

        Args:
        - position: The coordinates for drawing the cover. Default is (19, 13).
        """
        # Format the song ID
        cover_img_path = await self.asstes.get(AssetType.COVER, self.song_data.song_id)
        cover_img = Image.open(cover_img_path)

        cover_img = cover_img.convert("RGBA")
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
        type_img_path = self.asstes.generate_assets_path(
            f"{self.song_data.type.lower()}.png"
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
        ra_plate_img_path = self.asstes.generate_assets_path("ra_base.png")
        ra_plate_img = Image.open(ra_plate_img_path)
        ra_plate_img = ra_plate_img.resize((60, 32))

        font_ra = self.get_font(font_size)
        draw_ra_plate = ImageDraw.Draw(ra_plate_img)
        draw_ra_plate.text(
            (12, 7),
            str(self.song_data.rating),
            font=font_ra,
            fill=(255, 200, 0),
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            align="center",
        )
        self.main_img.paste(ra_plate_img, position, ra_plate_img)

    async def draw_song_rate(self, position=(10, 210), target_height=32):
        """
        Draw the song score.

        Args:
        - position: The coordinates for drawing the score. Default is (10, 210).
        - target_height: The target height for the score image. Default is 32.
        """
        if self.song_data.rating_icon:
            rate_img_path = await self.asstes.get(
                AssetType.RANK, self.song_data.rating_icon
            )
            rate_img = Image.open(rate_img_path)
            aspect_ratio = rate_img.width / rate_img.height
            target_width = int(target_height * aspect_ratio)
            rate_img = rate_img.resize((target_width, target_height))
            self.main_img.paste(rate_img, position, rate_img)

    def draw_song_ds(self, position=(138, 171), font_size=19):
        """
        Draw the song difficulty level.

        Args:
        - position: The coordinates for drawing the difficulty level.
        - font_size: The font size for the difficulty level.
        """
        draw_base = ImageDraw.Draw(self.main_img)
        draw_base.text(
            position,
            str(self.song_data.ds),
            font=self.get_font(font_size),
            fill=(255, 255, 255),
            stroke_width=2,
            stroke_fill=(0, 0, 0),
            align="center",
        )

    def draw_song_achievement(self, position=(75, 215), font_size=20):
        """
        Draw the song achievement.

        Args:
        - position: The coordinates for drawing the achievement. Default is (75, 215).
        - font_size: The font size for the achievement. Default is 20.
        """
        if self.song_data.achievements:
            draw_base = ImageDraw.Draw(self.main_img)
            draw_base.text(
                position,
                f"{self.song_data.achievements:.4f}",
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
        wrapped_text = textwrap.fill(
            str(self.song_data.title), width=11, break_long_words=True
        )
        draw_base = ImageDraw.Draw(self.main_img)
        draw_base.text(
            position,
            wrapped_text,
            font=self.get_font(font_size),
            fill=(255, 255, 255),
            stroke_width=2,
            stroke_fill=(0, 0, 0),
        )

    async def draw_song_badge(self, position=(135, 125)):
        """
        Draw the song badges.

        Args:
        - position: The coordinates for drawing the badges. Default is (135, 125).
        """
        x, y = position

        if self.song_data.fc:
            fc_img_path = await self.asstes.get(AssetType.BADGE, f"{self.song_data.fc}")
            fc_img = Image.open(fc_img_path)
            fc_img = fc_img.resize(
                (35, 35), resample=Image.Resampling.NEAREST
            )  # Using BILINEAR filter here
            self.paste(fc_img, (x, y))
            x -= 35

        if self.song_data.fs:
            fs_img_path = await self.asstes.get(AssetType.BADGE, f"{self.song_data.fs}")
            fs_img = Image.open(fs_img_path)
            fs_img = fs_img.resize(
                (35, 35), resample=Image.Resampling.NEAREST
            )  # Using BILINEAR filter here
            self.paste(fs_img, (x, y))

    async def draw(self):
        """
        Draw the song card.

        Args:
        - is_draw_title: Whether to draw the song title. Default is False.
        """

        # Draw the song cover
        await self.draw_song_cover()

        # Draw the song type
        self.draw_song_type()

        # Draw the song rank
        self.draw_song_rank()

        # Draw the song difficulty level
        self.draw_song_ds()

        # Draw the song rating
        await self.draw_song_rate()

        if self.is_draw_title:
            # Draw the song title
            self.draw_song_title()

        # Draw the song badges
        await self.draw_song_badge()

        # Draw the song achievement
        self.draw_song_achievement()

        return self.main_img
