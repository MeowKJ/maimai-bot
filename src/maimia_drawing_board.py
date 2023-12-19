import os.path
import random
import textwrap

from PIL import Image, ImageFont, ImageDraw
from src.util import generate_boolean_with_probability, has_only_common_characters, process_avatar, get_color_code, \
    draw_rainbow_text, get_color_code2


class MaimaiDrawingBoard:
    def __init__(self,
                 username,
                 avatar,
                 data,
                 is_draw_title=False,
                 is_compress_img=True,
                 maimai_assets_folder="./src/static/mai",
                 font_assets_folder="./src/static/mai/font",
                 en_font="BungeeInline-Regular.ttf",
                 jp_font="CusterMagic-Regular.ttf",
                 mix_font="happy.ttf",
                 ):
        # 初始化 MaimaiDrawingBoard 类的实例
        self.username = username
        self.avatar = avatar
        self.data = data
        self.is_draw_title = is_draw_title
        self.is_compress_img = is_compress_img
        self.maimai_assets_folder = maimai_assets_folder
        self.font_assets_folder = font_assets_folder
        self.en_font = en_font
        self.jp_font = jp_font
        self.mix_font = mix_font

        # 加载主图像模板 1 或 2 (10%) 作为主图像
        self.main_img = Image.open(f'./src/static/mai/img/main{2 if generate_boolean_with_probability(10) else 1}.png')

    def draw_song_plate(self, data, position_x, position_y):
        """
        在主图像上绘制歌曲信息。

        Args:
            data (dict): 包含歌曲数据的字典。
            position_x (int): 开始绘制歌曲的 X 坐标
            position_y  (int): 开始绘制歌曲的 Y 坐标
        """
        # 实现 draw_song_plate 方法的内容

        # 从 data 中获取歌曲数据
        achievements = data['achievements']
        ds = data['ds']
        fc = data['fc']
        fs = data['fs']
        level_index = data['level_index']
        ra = data['ra']
        rate = data['rate']
        song_id = data['song_id']
        title = data['title']
        _type = data['type']

        # 画歌曲框
        base_img_path = os.path.join(self.maimai_assets_folder, "song", "base", f"{level_index}.png")
        base_img = Image.open(base_img_path)
        base_img = base_img.resize((190, 252))

        # 画歌曲封面
        formatted_song_id = str(song_id).zfill(5)
        cover_img_path = os.path.join(self.maimai_assets_folder, "song", "cover", f"{formatted_song_id}.png")
        cover_img = Image.open(cover_img_path)
        cover_img = cover_img.resize((152, 152))
        base_img.paste(cover_img, (19, 13), cover_img)

        # 画歌曲类型
        type_img_path = os.path.join(self.maimai_assets_folder, "song", f"{_type.lower()}.png")
        type_img = Image.open(type_img_path)
        type_img = type_img.resize((85, 22))
        base_img.paste(type_img, (6, 3), type_img)

        # 画歌曲分数
        # 准备歌曲分数的底板
        ra_plate_img_path = os.path.join(self.maimai_assets_folder, "song", "ra_base.png")
        ra_plate_img = Image.open(ra_plate_img_path)
        ra_plate_img = ra_plate_img.resize((60, 32))

        # 画歌曲分数
        font_ra = ImageFont.truetype(os.path.join(self.font_assets_folder, self.en_font), 18)
        draw_ra_plate = ImageDraw.Draw(ra_plate_img)
        draw_ra_plate.text((12, 7), str(ra), font=font_ra, fill=(255, 200, 0), stroke_width=2, stroke_fill=(0, 0, 0),
                           align='center')
        base_img.paste(ra_plate_img, (130, 0), ra_plate_img)

        # 画歌曲定数
        font_ds = ImageFont.truetype(os.path.join(self.font_assets_folder, self.en_font), 19)
        draw_base = ImageDraw.Draw(base_img)
        draw_base.text((138, 171), str(ds), font=font_ds, fill=(255, 255, 255), stroke_width=2,
                       stroke_fill=(0, 0, 0),
                       align='center')

        # 画歌曲成绩图片
        if rate:
            rate_img_path = os.path.join(self.maimai_assets_folder, "song", "rank", f"{rate}.png")
            rate_img = Image.open(rate_img_path)
            target_height = 32
            aspect_ratio = rate_img.width / rate_img.height
            target_width = int(target_height * aspect_ratio)
            rate_img = rate_img.resize((target_width, target_height))
            base_img.paste(rate_img, (10, 210), rate_img)

        # 画歌曲达成率
        font_achievements = ImageFont.truetype(os.path.join(self.font_assets_folder, self.en_font), 20)
        draw_base.text((75, 215), "{:.4f}".format(achievements), font=font_achievements, fill=(255, 255, 255),
                       stroke_width=1, stroke_fill=(0, 0, 0), align='center')

        badges_x = 135
        if fc != "":
            fc_img_path = os.path.join(self.maimai_assets_folder, "song", "badges", f"{fc}_s.png")
            fc_img = Image.open(fc_img_path)
            base_img.paste(fc_img, (badges_x, 125), fc_img)
            badges_x -= 35

        if fs != "":
            fs_img_path = os.path.join(self.maimai_assets_folder, "song", "badges", f"{fs}_s.png")
            fs_img = Image.open(fs_img_path)
            base_img.paste(fs_img, (badges_x, 125), fs_img)

        # 画歌曲名字
        if self.is_draw_title:
            font_title = ImageFont.truetype(os.path.join(self.font_assets_folder, self.jp_font), 16)
            wrapped_text = textwrap.fill(str(title), width=11, break_long_words=True)

            draw_base.text((20, 25), wrapped_text, font=font_title, fill=(255, 255, 255), stroke_width=2,
                           stroke_fill=(0, 0, 0))
        self.main_img.paste(base_img, (position_x, position_y), base_img)

    def draw_songs(self, songs, is_b15, position_x, position_y):
        """
        在主图像上绘制歌曲信息。

        Args:
            songs (list): 包含歌曲数据的列表。
            is_b15 (bool): 标志歌曲是 B15 还是 B35。
            position_x (int): 开始绘制歌曲的 X 坐标。
            position_y (int): 开始绘制歌曲的 Y 坐标。
        """
        # 实现 draw_songs 方法的内容

    def draw_rocket_decor(self,position_x = 1192,position_y = 2643):
        """
        在主图像上绘制主人公角色。

        Args:
            position_x (int): 开始绘制火箭的 X 坐标。
            position_y (int): 开始绘制火箭的 Y 坐标。

        """
        # 实现 draw_character 方法的内容
        # 画火箭

        folder_path = os.path.join(self.maimai_assets_folder, "characters")
        image_path = os.path.join(folder_path, "rocket_small.png")
        character_img = Image.open(image_path)
        self.main_img.paste(character_img, (position_x, position_y), character_img)

    def draw_badge(self, position_x=1145, position_y=1725):
        """
        在主图像上绘制徽章。

        Args:
            position_x (int): 开始绘制徽章的 X 坐标。
            position_y (int): 开始绘制徽章的 Y 坐标。
        """
        # 实现 draw_secondary_character 方法的内容
        folder_path = os.path.join(self.maimai_assets_folder, "characters")
        random_number = random.randint(0, 16)
        image_path = os.path.join(folder_path, f"yj{random_number}.png")
        character_img = Image.open(image_path)

        self.main_img.paste(character_img, (position_x, position_y), character_img)

    async def draw_plate(self, rating, name, avatar):
        """
        在主图像上绘制包含用户信息的板块。

        Args:
            rating (int): 用户分数。
            name (str): 用户名。
            avatar (Image): 用户头像。
        """
        # 获取板块图片
        folder_path = os.path.join(self.maimai_assets_folder, "plate", "raw")
        plate_image_files = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
        random_image = random.choice(plate_image_files)
        image_path = os.path.join(folder_path, random_image)
        plate_img = Image.open(image_path)
        plate_img = plate_img.resize((1160, 200))

        # 获取分数板块图片
        dx_rating_plate_img = Image.open(
            os.path.join(self.maimai_assets_folder, "dx_rating",
                         f"UI_CMN_DXRating_S_{get_color_code(rating)}_waifu2x_2x_png.png")
        )
        dx_rating_plate_img = dx_rating_plate_img.resize((348, 72))
        plate_img.paste(dx_rating_plate_img, (200, 17), dx_rating_plate_img)

        # 获取姓名板块图片
        name_plate_img = Image.open(os.path.join(self.maimai_assets_folder, "img", "name.png"))
        plate_img.paste(name_plate_img, (200, 99), name_plate_img)

        # 如果有头像，粘贴头像到板块图片上
        if avatar:
            avatar_pic = await process_avatar(avatar)
            plate_img.paste(avatar_pic, (7, 8), avatar_pic)

        draw_ra_plate = ImageDraw.Draw(plate_img)
        name = str(name)
        # 根据名字内容选择字体
        if has_only_common_characters(name):
            en_font = ImageFont.truetype(os.path.join(self.font_assets_folder, self.en_font), 48)
        else:
            en_font = ImageFont.truetype(os.path.join(self.font_assets_folder, self.mix_font), 48)

        draw_ra_plate.text((212, 115), name, font=en_font, fill=(0, 0, 0))

        en_font_36 = ImageFont.truetype(os.path.join(self.font_assets_folder, self.en_font), 34)
        draw_ra_plate.text((375, 37), " ".join(str(rating)), font=en_font_36, fill=(255, 215, 0), stroke_width=2,
                           stroke_fill=(0, 0, 0), align='center')
        self.main_img.paste(plate_img, (120, 75), plate_img)

    def draw_score_nv(self, b15_scores, b35_scores, position_x=315, position_y=290):
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
        nv_img = Image.open(os.path.join(self.maimai_assets_folder, "img", "title_base.png"))
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

        self.main_img.paste(nv_img, (position_x, position_y), nv_img)

    def draw_footer(self, b15_songs, b35_songs):
        """
        在主图像上绘制包含歌曲信息的页脚。

        Args:
            b15_songs (list): 包含 B15 歌曲数据的列表。
            b35_songs (list): 包含 B35 歌曲数据的列表。
        """
        # 实现 draw_footer 方法的内容
        pass


    def get_font(self, font_size=36):
        """
        获取字体。

        Returns:
            ImageFont: 字体。
        """
        return ImageFont.truetype(os.path.join(self.font_assets_folder, self.jp_font), 36)