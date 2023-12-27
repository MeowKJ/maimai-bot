import aiohttp
from typing import List

from src.util.context import app_config
from src.data.song import SongData

api_secret = app_config["api_secret"]


class Player:
    def __init__(
        self,
        username,
        guild_id,
        avatar_url,
    ):
        """
        Initializes a Player object.

        Args:
            username (str): The username of the player.
            guild_id (int): The ID of the guild the player belongs to.
            icon_url (str): The URL of the player's icon.
        """
        self.username = username
        self.guild_id = guild_id

        self.avatar_url = avatar_url

        self.nickname = username
        self.rating = 0

        self.course_rank = None
        self.class_rank = None
        self.name_plate = None
        self.star = None

        self.song_data_b15: List[SongData] = []
        self.song_data_b35: List[SongData] = []

        self.song_data_b15_total = 0
        self.song_data_b35_total = 0

    async def fetch_divingfish(self):
        """
        Fetches data from Diving Fish.
        """
        async with aiohttp.request(
            "POST",
            "https://www.diving-fish.com/api/maimaidxprober/query/player",
            json={"username": self.username, "b50": True},
        ) as resp:
            if resp.status == 200:
                obj = await resp.json()
                self.nickname = obj["nickname"]
                self.rating = obj["rating"]
                for i in obj["charts"]["dx"]:
                    song_data = SongData.from_data_divingfish(i)
                    self.song_data_b15_total += song_data.rating
                    self.song_data_b15.append(song_data)

                for i in obj["charts"]["sd"]:
                    song_data = SongData.from_data_divingfish(i)
                    self.song_data_b35_total += song_data.rating
                    self.song_data_b35.append(song_data)

                return 200, ""
            else:
                return resp.status, "无法从水鱼查分器获取你的数据"

    async def fetch_luoxue(self):
        """
        Fetches data from Luo Xue.
        """
        base_api = "https://maimai.lxns.net"
        auth_headers = {
            "Authorization": api_secret,
        }
        obj = None
        async with aiohttp.request(
            "GET",
            base_api + "/api/v0/maimai/player/qq/" + str(self.username),
            headers=auth_headers,
        ) as resp:
            if resp.status != 200:
                return resp.status, "爆炸了"
            obj = await resp.json()
            if obj["code"] == 403:
                return 403, "发现没有开启选项[允许读取玩家信息]"
            elif obj["code"] == 404:
                return 404, f"未能找到[{self.username}]的数据, 请检查落雪查分器中绑定的QQ号是否一致"
            elif obj["code"] != 200:
                return obj["code"], "暂时无法查询到您的b50"

            self.nickname = obj["data"]["name"]
            self.rating = obj["data"]["rating"]
            self.class_rank = obj["data"]["class_rank"]
            self.course_rank = obj["data"]["course_rank"]
            self.star = obj["data"]["star"]
            self.avatar_url = obj["data"]["icon_url"]
            friend_code = obj["data"]["friend_code"]
            self.name_plate = obj["data"]["name_plate"]["id"]

        async with aiohttp.request(
            "GET",
            base_api + "/api/v0/maimai/player/" + str(friend_code) + "/bests",
            headers=auth_headers,
        ) as resp:
            if resp.status != 200:
                return resp.status, "爆炸了"
            obj = await resp.json()
            if obj["code"] == 403:
                return 403, "发现没有开启选项[允许读取谱面成绩]"
            elif obj["code"] != 200:
                return obj["code"], "暂时无法查询到您的b50"
            for i in obj["data"]["standard"]:
                song_data = SongData.from_data_luoxue(i)
                self.song_data_b35.append(song_data)

            for i in obj["data"]["dx"]:
                song_data = SongData.from_data_luoxue(i)
                self.song_data_b15.append(song_data)

            self.song_data_b15_total = obj["data"]["dx_total"]
            self.song_data_b35_total = obj["data"]["standard_total"]

            return 200, ""
