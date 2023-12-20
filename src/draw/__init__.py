"""
This module contains the functions for generating maimai images.
"""
import os
import time

import aiohttp


from src.util.database import get_user_name_by_id, get_user_score, update_user_score
from src.draw.maimai_drawing_board import MaimaiDrawingBoard
from src.util.tools import generate_boolean_with_probability
from src.util.context import context


async def generate_b50(
    userid, avatar, params, output_path=os.path.join(context["assets_path"], "images")
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
    if username is None:
        return "发现你还没有绑定水鱼查分器用户名，发送/bind + 用户名，就可以绑定了", 404
    payload = {"username": username, "b50": True}

    async with aiohttp.request(
        "POST",
        "https://www.diving-fish.com/api/maimaidxprober/query/player",
        json=payload,
    ) as resp:
        if resp.status == 400:
            return f"在水鱼查封器中不存在[{username}]的用户，请检查是否填写了错误的用户名", 404
        if resp.status == 403:
            return "没有权限查询的您的b50,如果需要查询请在查分器中开启权限", 300
        if resp.status == 200:
            obj = await resp.json()
        else:
            return "水鱼查分器出现了一些问题,暂时无法查询到您的b50", 500

        if "o" in params:
            target_path = os.path.join(output_path, f"{username}_origin.png")
        else:
            target_path = os.path.join(output_path, f"{username}.png")
        target_path = os.path.normpath(target_path)
        if "f" not in params:
            if get_user_score(userid) == obj["rating"]:
                if os.path.exists(target_path):
                    return (target_path, 0), 201
        update_user_score(userid, obj["rating"])
        main_img_path = os.path.join(
            context["assets_path"],
            "img",
            "main2.png" if generate_boolean_with_probability(10) else "main1.png",
        )
        maimai_pic = MaimaiDrawingBoard(
            main_img_path=main_img_path,
            avatar=avatar,
            data=obj,
            is_draw_title=False,
            is_compress_img=True,
            username=username,  # Pass the 'username' argument to the constructor
        )
        await maimai_pic.draw()
        maimai_pic.save(target_path)
        time_end = time.time()
        return (target_path, time_end - time_start), 200