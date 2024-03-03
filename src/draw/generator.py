"""
This module contains the functions for generating maimai images.
"""

import os
import time
from botpy import logger
import aiohttp

from src.database.database_manager import (
    get_name_score_by_id,
    update_score_by_id,
)
from src.draw.maimai_drawing_board import MaimaiDrawingBoard
from src.utils.app_config import config
from src.utils.common_utils import (
    generate_boolean_with_probability,
    is_valid_luoxue_username,
)
from src.utils.compress_utils import compress_png
from .data_models.player import Player


async def heartbeat_request(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            if response.status == 200:
                print("Heartbeat request successful!")
            else:
                print("Heartbeat request failed.")


async def generate_b50(
    userid,
    avatar_url,
    params,
    output_path=os.path.join(config.static_config["assets_path"], "images"),
):
    """
    Generate a maimai image with b50 information.

    Args:
        userid (str): The user ID.
        avatar_url (str): The avatar image path.
        params (list): Additional parameters for image generation.
        output_path (str, optional): The output path for the generated image.
            Defaults to os.path.join(context["assets_path"], "images").

    Returns:
        tuple: A tuple containing the path to the generated image and the execution time.

    Raises:
        int: The HTTP status code indicating the result of the generation process.
    """
    time_start = time.time()
    username, score = await get_name_score_by_id(userid)

    is_use_origin = "o" in params
    is_force_generate = "f" in params

    if username is None:
        return (
            404,
            (
                "发现你还没有绑定查分器用户名\n"
                "发送/bind + 水鱼查分器用户名,就可以绑定水鱼查分器\n"
                "或者发送/bind + QQ号,就可以绑定落雪咖啡屋查分器"
            ),
            None,
        )

    player = Player(
        username=username,
        guild_id=userid,
        avatar_url=avatar_url,
        api_secret=config.bot_config["api_secret"],
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
    if not is_force_generate and os.path.exists(target_path) and score == player.rating:
        return 201, "你的DX Rating没有变化", target_path

    # 更新玩家rating
    await update_score_by_id(userid, player.rating)

    # 准备背景图片
    main_img_path = os.path.join(
        config.static_config["assets_path"],
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

    if compression_ratio is None:
        target_path = origin_path
        logger.error("压缩失败 -- %s", compress_path)

    logger.info("压缩比: %.2f%%", compression_ratio)

    time_end = time.time()

    msg += f"生成成功，用时{time_end - time_start:.2f}s"
    await heartbeat_request(config.heartbeat_url)
    return 200, msg, target_path
