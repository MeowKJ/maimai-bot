import os
import random
import textwrap
from datetime import datetime

from src.draw.util import *


def draw_songs(songs, main_img, is_b15, is_draw_title):
    # 画歌曲
    x = 0
    y = 0
    if is_b15:
        position_x = 100
        position_y = 2050
    else:
        position_x = 100
        position_y = 405
    for i in songs:
        achievements = i['achievements']
        ds = i['ds']
        fc = i['fc']
        fs = i['fs']
        level_index = i['level_index']
        ra = i['ra']
        rate = i['rate']
        song_id = i['song_id']
        title = i['title']
        _type = i['type']

        # 画歌曲框
        base_img_path = f'./src/static/mai/song/base/{level_index}.png'
        base_img = Image.open(base_img_path)
        base_img = base_img.resize((190, 252))

        # 画歌曲封面
        formatted_song_id = str(song_id).zfill(5)
        cover_img_path = f'./src/static/mai/song/cover/{formatted_song_id}.png'
        cover_img = Image.open(cover_img_path)
        cover_img = cover_img.resize((152, 152))
        base_img.paste(cover_img, (19, 13), cover_img)

        # 画歌曲类型
        type_img_path = f'./src/static/mai/song/{_type.lower()}.png'
        type_img = Image.open(type_img_path)
        type_img = type_img.resize((85, 22))
        base_img.paste(type_img, (6, 3), type_img)

        # 画歌曲分数
        ra_plate_img = Image.open(f'./src/static/mai/song/UI_MSS_Genre_Base_01.png')
        ra_plate_img = ra_plate_img.resize((60, 32))
        font = ImageFont.truetype('./src/static/font/BungeeInline-Regular.ttf', 18)
        draw_ra_plate = ImageDraw.Draw(ra_plate_img)
        draw_ra_plate.text((12, 7), str(ra), font=font, fill=(255, 200, 0), stroke_width=2, stroke_fill=(0, 0, 0),
                           align='center')
        base_img.paste(ra_plate_img, (130, 0), ra_plate_img)

        # 画歌曲难度
        font_ds = ImageFont.truetype('./src/static/font/BungeeInline-Regular.ttf', 19)
        draw_base = ImageDraw.Draw(base_img)
        draw_base.text((138, 171), str(ds), font=font_ds, fill=(255, 255, 255), stroke_width=2, stroke_fill=(0, 0, 0),
                       align='center')

        # 画歌曲成就
        if rate != "":
            rate_img_path = f'./src/static/mai/song/rank/{rate}.png'
            rate_img = Image.open(rate_img_path)
            target_height = 32
            aspect_ratio = rate_img.width / rate_img.height
            target_width = int(target_height * aspect_ratio)
            rate_img = rate_img.resize((target_width, target_height))
            base_img.paste(rate_img, (10, 210), rate_img)
        font_achievements = ImageFont.truetype('./src/static/font/BungeeInline-Regular.ttf', 20)
        draw_base.text((75, 215), "{:.4f}".format(achievements), font=font_achievements, fill=(255, 255, 255),
                       stroke_width=1, stroke_fill=(0, 0, 0), align='center')

        badges_x = 135
        if fc != "":
            fc_img_path = f'./src/static/mai/song/badges/{fc}_s.png'
            fc_img = Image.open(fc_img_path)
            # fc_img = fc_img.resize((40, 40))
            base_img.paste(fc_img, (badges_x, 125), fc_img)
            badges_x -= 35

        if fs != "":
            fs_img_path = f'./src/static/mai/song/badges/{fs}_s.png'
            fs_img = Image.open(fs_img_path)
            # fs_img = fs_img.resize((40, 40))
            base_img.paste(fs_img, (badges_x, 125), fs_img)

        # 画歌曲名字
        if is_draw_title:
            font_title = ImageFont.truetype('./src/static/font/CusterMagic-Regular.ttf', 16)
            wrapped_text = textwrap.fill(str(title), width=11, break_long_words=True)

            draw_base.text((20, 25), wrapped_text, font=font_title, fill=(255, 255, 255), stroke_width=2,
                           stroke_fill=(0, 0, 0))

        main_img.paste(base_img, (position_x, position_y), base_img)
        x = x + 1

        if is_b15:
            position_x = position_x + 203
            if x == 6:
                y = y + 1
                position_x = 100
                position_y = position_y + 267
                x = 0
        else:
            position_x = position_x + 203
            if x == 6:
                y = y + 1
                position_x = 100
                position_y = position_y + 267
                x = 0


def draw_character(main_img):
    # 画人物
    folder_path = './src/static/mai/characters'
    rocket_dila = "rocket_small.png"
    image_path = os.path.join(folder_path, rocket_dila)
    character_img = Image.open(image_path)
    main_img.paste(character_img, (1192, 2634), character_img)


def draw_secondary_character(main_img):
    # 画次要人物
    folder_path = './src/static/mai/characters'
    random_number = random.randint(0, 16)
    image_path = os.path.join(folder_path, f"yj{random_number}.png")
    character_img = Image.open(image_path)

    main_img.paste(character_img, (1145, 1725), character_img)


async def draw_plate(main_img, avatar, name, rating):
    # 画姓名框、分数框、头像
    folder_path = './src/static/mai/plate/raw'
    plate_image_files = [f for f in os.listdir(folder_path) if f.endswith(('png', 'jpg', 'jpeg', 'gif', 'bmp'))]
    random_image = random.choice(plate_image_files)
    image_path = os.path.join(folder_path, random_image)
    plate_img = Image.open(image_path)
    plate_img = plate_img.resize((1160, 200))

    dx_rating_plate_img = Image.open(
        f'./src/static/mai/dx_rating/UI_CMN_DXRating_S_{get_color_code(rating)}_waifu2x_2x_png.png')
    dx_rating_plate_img = dx_rating_plate_img.resize((348, 72))
    plate_img.paste(dx_rating_plate_img, (200, 17), dx_rating_plate_img)

    name_plate_img = Image.open(f'./src/static/mai/img/name.png')
    plate_img.paste(name_plate_img, (200, 99), name_plate_img)

    if avatar:
        avatar_pic = await process_avatar(avatar)
        plate_img.paste(avatar_pic, (7, 8), avatar_pic)

    draw_ra_plate = ImageDraw.Draw(plate_img)
    name = str(name)
    if has_only_common_characters(name):
        en_font = ImageFont.truetype('./src/static/font/BungeeInline-Regular.ttf', 48)
    else:
        en_font = ImageFont.truetype('./src/static/font/happy.ttf', 48)

    draw_ra_plate.text((212, 115), name, font=en_font, fill=(0, 0, 0))

    en_font_36 = ImageFont.truetype('./src/static/font/BungeeInline-Regular.ttf', 34)
    draw_ra_plate.text((375, 37), " ".join(str(rating)), font=en_font_36, fill=(255, 215, 0), stroke_width=2,
                       stroke_fill=(0, 0, 0), align='center')
    main_img.paste(plate_img, (120, 75), plate_img)


def draw_score_nv(main_img, b15_scores, b35_scores):
    x = 130
    y = 35
    b15_scores_q = b15_scores * 50 / 15
    b35_scores_q = b35_scores * 50 / 35
    font_path = './src/static/font/BungeeInline-Regular.ttf'
    font_size = 36

    # Create a blank image for drawing
    nv_img = Image.open(f'./src/static/mai/img/title_base.png')
    draw_f = ImageDraw.Draw(nv_img)

    # Add rainbow effect for scores greater than 15000
    if b15_scores_q > 15000:
        draw_rainbow_text(nv_img, (x, y), f"B15 -> {b15_scores}", font_path, font_size)
    else:
        draw_text(draw_f, (x, y), f"B15 -> {b15_scores}", get_color_code2(b15_scores_q), font_path, font_size)

    if b35_scores_q > 15000:
        draw_rainbow_text(nv_img, (x + 270, y), f"B35 -> {b35_scores}", font_path, font_size)
    else:
        draw_text(draw_f, (x + 270, y), f"B35 -> {b35_scores}", get_color_code2(b35_scores_q), font_path,
                  font_size)
    main_img.paste(nv_img, (315, 290), nv_img)


def draw_footer(main_img, b15, b35):
    # 画页脚
    footer_img_list = ["UI_footer1.png", "UI_footer2.png", "UI_footer3.png"]
    footer_img_path = random.choice(footer_img_list)
    footer_img = Image.open(f'./src/static/mai/img/{footer_img_path}')
    draw_f = ImageDraw.Draw(footer_img)
    font = ImageFont.truetype('./src/static/font/BungeeInline-Regular.ttf', 30)

    if footer_img_path == "UI_footer2.png":
        x = 60
        y = 100
    elif footer_img_path == "UI_footer3.png":
        x = 65
        y = 75
    else:
        y = 75
        x = 40
    if b15:
        b15_max = b15[0]["ra"]
        b15_min = b15[-1]["ra"]
        draw_f.text((x, y), f"B15 -> MAX {b15_max} MIN {b15_min}", font=font, fill=(0, 0, 0))

    if b35:
        b35_max = b35[0]["ra"]
        b35_min = b35[-1]["ra"]
        draw_f.text((x, y := y + 50), f"B35 -> MAX {b35_max} MIN {b35_min}", font=font, fill=(0, 0, 0))

    font = ImageFont.truetype('./src/static/font/BungeeInline-Regular.ttf', 23)
    current_time = datetime.now()

    # 将时间格式化为 "xx/xx/xx" 的形式
    formatted_time = current_time.strftime("%Y/%m/%d")
    draw_f.text((x, y := y + 50), f"{formatted_time}", font=font, fill=(0, 0, 0))
    font = ImageFont.truetype('./src/static/font/zh_yuan.otf', 20)
    draw_f.text((x, y + 30), f"Generated by Maimai的频道 Bot", font=font, fill=(0, 0, 0))

    main_img.paste(footer_img, (750, 2600), footer_img)


async def draw(username, avatar, data, is_draw_title=False):
    random_number = random.randint(1, 10)
    # 如果生成的是10，将其作为2处理
    if random_number == 10:
        random_number = 2
    else:
        random_number = 1
    main_img = Image.open(f'./src/static/mai/img/main{random_number}.png')
    draw_secondary_character(main_img)
    await draw_plate(main_img, avatar, data['nickname'], data['rating'])

    b15_songs = data['charts']['dx']

    b15_score = 0
    b35_score = 0

    if len(b15_songs):
        for i in b15_songs:
            b15_score += i['ra']
        draw_songs(b15_songs, main_img, True, is_draw_title)

    b35_songs = data['charts']['sd']
    if len(b35_songs):
        for i in b35_songs:
            b35_score += i['ra']
        draw_songs(b35_songs, main_img, False, is_draw_title)

    draw_score_nv(main_img, b15_score, b35_score)
    # draw_hr(main_img)
    draw_footer(main_img, b15_songs, b35_songs)
    draw_character(main_img)

    main_img.save(os.path.join(pic_path, f'{username}.png'))
    return os.path.join(pic_path, f'{username}.png')
