import os.path
import random
import textwrap
import datetime
from PIL import Image, ImageFont, ImageDraw
from src.util import generate_boolean_with_probability, has_only_common_characters, process_avatar, get_color_code, \
    draw_rainbow_text, get_color_code2

from src.draw.drawing_board import DrawingBoard
from src.draw.song_drawing_board import SongDrawingBoard
from src.draw.profile_drawing_board import ProfileDrawingBoard

class MaimaiDrawingBoard(DrawingBoard):
    def __init__(self,
                 main_img,
                 username,
                 avatar,
                 data,
                 is_draw_title=False,
                 is_compress_img=True,
                 ):
        """
        初始化 MaimaiDrawingBoard 类的实例

        Args:
            main_img (PIL.Image.Image): 主图像
            username (str): 用户名
            avatar (str): 头像路径
            data (dict): 包含绘制数据的字典
            is_draw_title (bool, optional): 是否绘制标题，默认为 False
            is_compress_img (bool, optional): 是否压缩图像，默认为 True
        """
        super().__init__(main_img=main_img)
        self.username = username
        self.avatar = avatar
        self.data = data

        self.is_draw_title = is_draw_title
        self.is_compress_img = is_compress_img
        
        self.b15_songs = data["charts"]["dx"]
        self.b35_songs = data["charts"]["sd"]
        self.b15_score = 0
        self.b15_score = 0

    def draw_songs(self, is_b15, position_b15 = (100, 2050), position_b35 = (100, 405)):
        """
        在主图像上绘制歌曲信息。

        Args:
            songs (list): 包含歌曲数据的列表。
            is_b15 (bool): 标志歌曲是 B15 还是 B35。
            position (tuple): 开始绘制歌曲的位置坐标 (position_x, position_y)。
        """
        if is_b15:
            song_data_list = self.b15_songs
            position = position_b15
            position_x = position_b15[0]
            position_y = position_b15[1]
        else:
            song_data_list = self.b35_songs
            position = position_b35
            position_x = position_b35[0]
            position_y = position_b35[1]
        x, y = 0
        score = 0
        for song_data in song_data_list:
            score += song_data["ra"]
            song_plate = SongDrawingBoard(song_data)
            song_plate.draw(self.is_draw_title)
            self.paste(song_plate, position)
            x = x + 1
            position_x = position_x + 203
            if x == 6:
                y = y + 1
                position_x = position[0]
                position_y = position_y + 267
                x = 0
        
        if is_b15:
            self.b15_score = score
        else:
            self.b35_score = score
            
            

    def draw_rocket_decor(self, position=(1192, 2643)):
        """
        在主图像上绘制主人公角色。

        Args:
            position (tuple, optional): 开始绘制火箭的位置坐标 (position_x, position_y)。默认为 (1192, 2643)。
        """
        # 实现 draw_character 方法的内容
        # 画火箭

        folder_path = os.path.join(self.maimai_assets_folder, "characters")
        image_path = os.path.join(folder_path, "rocket_small.png")
        character_img = Image.open(image_path)
        self.main_img.paste(character_img, position, character_img)

    def draw_badge(self, position=(1145, 1725)):
        """
        在主图像上绘制徽章。

        Args:
            position (tuple, optional): 开始绘制徽章的位置坐标 (position_x, position_y)。默认为 (1145, 1725)。
        """
        # 实现 draw_secondary_character 方法的内容
        folder_path = os.path.join(self.maimai_assets_folder, "characters")
        random_number = random.randint(0, 16)
        image_path = os.path.join(folder_path, f"yj{random_number}.png")
        character_img = Image.open(image_path)

        self.main_img.paste(character_img, position, character_img)

    async def draw_profile_plate(self, rating, name, avatar, position=(120, 75)):
        """
        在主图像上绘制包含用户信息的板块。

        Args:
            rating (int): 用户分数。
            name (str): 用户名。
            avatar (Image): 用户头像。
        """
        # 实现 draw_plate 方法的内容
        profile_plate = ProfileDrawingBoard(self.main_img, rating, name, avatar)
        await profile_plate.draw()
        self.paste(profile_plate, (120, 75))



    def draw_score_nv(self, b15_scores, b35_scores, position=(315, 290)):
        """
        在主图像上绘制 B15 和 B35 分数信息。

        Args:
            b15_scores (int): B15 分数。
            b35_scores (int): B35 分数。
            position_x (int): 开始绘制分数的 X 坐标。
            position_y (int): 开始绘制分数的 Y 坐标。
        """
        x = 130
        y = 35
        b15_scores_q = b15_scores * 50 / 15
        b35_scores_q = b35_scores * 50 / 35
        font_size = 36

        # 创建一个用于绘制的空白图像
        nv_img = Image.open(os.path.join(self.assets_path, "img", "title_base.png"))
        draw_f = ImageDraw.Draw(nv_img)

        # 添加彩虹效果，用于分数大于 15000
        if b15_scores_q > 15000:
            draw_rainbow_text(nv_img, (x, y), f"B15 -> {b15_scores}", self.font_assets_folder, font_size)
        else:
            draw_f.text((x, y), f"B15 -> {b15_scores}", font=self.get_font(), fill=self.get_color_code2(b15_scores_q),
                        stroke_width=2, stroke_fill=(0, 0, 0))

        if b35_scores_q > 15000:
            draw_rainbow_text(nv_img, (x + 270, y), f"B35 -> {b35_scores}", self.font_assets_folder, font_size)
        else:
            draw_f.text((x + 270, y), f"B35 -> {b35_scores}", font=self.get_font(),
                        fill=get_color_code2(b15_scores_q), stroke_width=2, stroke_fill=(0, 0, 0))

        self.main_img.paste(nv_img, position, nv_img)


    def draw_footer(self, position= (750, 2600)):
        """
        在主图像上绘制包含歌曲信息的页脚。
        """
        # 实现 draw_footer 方法的内容
         # 画页脚
        footer_img_list = ["UI_footer1.png", "UI_footer2.png", "UI_footer3.png"]
        footer_img_path = random.choice(footer_img_list)
        footer_img = Image.open(os.path.join(self.assets_path, "img", footer_img_path))
        draw_f = ImageDraw.Draw(footer_img)
        font = self.get_font(font_size=30)

        if footer_img_path == "UI_footer2.png":
            x = 60
            y = 100
        elif footer_img_path == "UI_footer3.png":
            x = 65
            y = 75
        else:
            y = 75
            x = 40
        if self.b15_score > 0:
            b15_max = self.b15_songs[0]["ra"]
            b15_min = self.b15_songs[-1]["ra"]
            draw_f.text((x, y), f"B15 -> MAX {b15_max} MIN {b15_min}", font=font, fill=(0, 0, 0))

        if self.b35_score > 0:
            b35_max = self.b35_songs[0]["ra"]
            b35_min = self.b35_songs[-1]["ra"]
            draw_f.text((x, y := y + 50), f"B35 -> MAX {b35_max} MIN {b35_min}", font=font, fill=(0, 0, 0))

        font = self.get_font(font_size=23)
        current_time = datetime.now()

        # 将时间格式化为 "xx/xx/xx" 的形式
        formatted_time = current_time.strftime("%Y/%m/%d")
        draw_f.text((x, y := y + 50), f"{formatted_time}", font=font, fill=(0, 0, 0))
        font = ImageFont.truetype('./src/static/font/zh_yuan.otf', 20)
        draw_f.text((x, y + 30), f"Generated by Maimai的频道 Bot", font=font, fill=(0, 0, 0))

        self.paste(footer_img,position)

    def draw(self):
        self.draw_profile_plate(self.data["rating"], self.username, self.avatar)
        self.draw_songs(self.is_draw_title)
        self.draw_footer()
        self.draw_rocket_decor()

