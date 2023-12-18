from src.draw.draw import draw
from src.draw.db import get_user_name_by_id, get_user_score, updata_user_score
import aiohttp
import os


async def generate50(userid, avatar, params, pic_path="./src/static/mai/images"):
    username = get_user_name_by_id(userid)
    if username is None:
        return "发现你还没有绑定水鱼查分器用户名，发送/bind + 用户名，就可以绑定了", 404
    payload = {'username': username, 'b50': True}

    async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player",
                               json=payload) as resp:
        if resp.status == 400:
            return f"在水鱼查封器中不存在[{username}]的用户，请检查是否填写了错误的用户名", 404
        if resp.status == 403:
            return f"没有权限查询的您的b50，如果需要查询请在查分器中开启权限", 300
        if resp.status == 200:
            obj = await resp.json()
        else:
            return "水鱼查分器出现了一些问题，暂时无法查询到您的b50", 500
        if "f" not in params:
            if get_user_score(userid) == obj['rating']:
                if os.path.exists(os.path.join(pic_path, f"{username}.png")):
                    return os.path.join(pic_path, f"{username}.png"), 201
            updata_user_score(userid, obj['rating'])
        pic = await draw(payload['username'], avatar, obj, is_draw_title="n" in params)

        return pic, 200
