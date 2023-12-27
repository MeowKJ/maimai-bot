"""
This module contains the functions for generating maimai images.
"""
import os
import time

import aiohttp


from src.util.database import get_user_name_by_id, get_user_score, update_user_score
from src.draw.maimai_drawing_board import MaimaiDrawingBoard
from src.util.tools import generate_boolean_with_probability, is_valid_luoxue_username
from src.util.context import context, logger
from src.util.compress import compress_png

from src.data.player import Player


async def generate_b50(
    userid,
    avatar_url,
    params,
    output_path=os.path.join(context["assets_path"], "images"),
):
    """
    Generate a maimai image with b50 information.

    Args:
        userid (int): The user ID.
        avatar (str): The avatar image path.
        params (str): Additional parameters for image generation.
        output_path (str, optional): The output path for the generated image.
            Defaults to os.path.join(context["assets_path"], "images").

    Returns:
        tuple: A tuple containing the path to the generated image and the execution time.

    Raises:
        int: The HTTP status code indicating the result of the generation process.
    """
    time_start = time.time()
    username = get_user_name_by_id(userid)

    is_use_origin = "o" in params
    is_force_generate = "f" in params

    if username is None:
        return (
            404,
            """发现你还没有绑定查分器用户名
发送/bind + 水鱼查分器用户名,就可以绑定水鱼查分器
或者发送/bind + QQ号,就可以绑定落雪咖啡屋查分器""",
            None,
        )

    player = Player(
        username=username,
        guild_id=userid,
        avatar_url=avatar_url,
    )

    if is_valid_luoxue_username(username):
        code, msg = await player.fetch_luoxue()
        msg = "[落雪咖啡屋]" + msg
    else:
        code, msg = await player.fetch_divingfish()
        msg = "[水鱼查分器]" + msg
    if code != 200:
        return code, msg, None

    # 获取目标路径
    target_path = os.path.join(
        output_path, f'{username}{"_origin" if is_use_origin else ""}.png'
    )
    target_path = os.path.normpath(target_path)

    # 是否强制生成
    if (
        not is_force_generate
        and os.path.exists(target_path)
        and get_user_score(userid) == player.rating
    ):
        return 201, "你的DX Rating没有变化", target_path

    # 更新玩家rating
    update_user_score(userid, player.rating)

    # 准备背景图片
    main_img_path = os.path.join(
        context["assets_path"],
        "img",
        "main2.png" if generate_boolean_with_probability(10) else "main1.png",
    )

    # 开始绘画
    maimai_pic = MaimaiDrawingBoard(
        main_img_path=main_img_path,
        player=player,
        is_draw_title=False,
        is_compress_img=True,
    )
    await maimai_pic.draw()
    maimai_pic.main_img.convert("RGB")

    origin_path = os.path.join(output_path, f"{username}_origin.png")
    maimai_pic.save(origin_path)

    compress_path = os.path.join(output_path, f"{username}.png")
    compression_ratio = await compress_png(origin_path, compress_path)
    logger.info(f"压缩比: {compression_ratio}%")

    time_end = time.time()
    msg += f"生成成功，用时{time_end - time_start:.2f}s"
    return 200, msg, target_path
