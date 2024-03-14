"""
guess_song.py
"""

import os
import asyncio
import random
import time
import tempfile
from collections import Counter

import aiohttp

from botpy import Client, logger
from botpy.message import Message
from PIL import Image
from src.assets_generator.get_assets import Assets, AssetType
from src.common.alias import get_alias_by_id
from src.utils.app_config import config
from src.utils.common_utils import get_version_name


class GuessSongHandler:
    """
    处理猜歌游戏的类，每个频道(guild)同时只能运行一个游戏实例。
    """

    _instances = {}  # 存储每个 guild 的游戏实例

    def __new__(cls, client: Client, message: Message):
        """
        确保每个 guild 只有一个实例。
        """
        guild_id = message.guild_id
        if guild_id in cls._instances:
            return cls._instances[guild_id]
        else:
            instance = super(GuessSongHandler, cls).__new__(cls)
            cls._instances[guild_id] = instance
            return instance

    def __init__(self, client: Client, message: Message):
        """
        初始化游戏处理器。
        """
        self.client = client
        self.message = message
        guild_id = message.guild_id

        if hasattr(self, "initialized"):
            # 防止重复初始化
            return
        self.guild = guild_id
        self.temp_files = []
        self.current_song = None
        self.alias_str = ""
        self.game_active = False
        self.initialized = True

    def __del__(self):
        """
        清理临时文件和实例。
        """
        for temp_file in self.temp_files:
            try:
                os.remove(temp_file)
            except OSError:
                pass
        if self.guild in self._instances:
            del self._instances[self.guild]

    async def start_game(self, msg_id):
        """
        开始猜歌游戏。
        """
        if self.game_active:
            await self.send_message("一个游戏已经在进行中了！", msg_id)
            return
        self.game_active = True
        self.current_song = await self.choice_song()
        self.alias_str = await get_alias_by_id(self.current_song["id"])
        cover_path = await self.get_cover()
        print(cover_path)
        await self.send_message("请猜这首歌曲的名字！", msg_id, image=cover_path)
        await self.wait_for_guess()

    async def send_message(self, content, msg_id, image=None):
        """
        发送消息到指定频道。
        """
        channel_id = self.message.channel_id
        await self.client.api.post_message(
            channel_id=channel_id, content=content, msg_id=msg_id, file_image=image
        )

    async def guess_song(self, message, msg_id):
        """
        处理用户的猜歌尝试。
        """
        if not self.game_active:
            return

        if await self.judge_guess(message):
            await self.send_message("恭喜你猜对了！", msg_id)
            await self.end_game()
        else:
            await self.send_message("猜错了，再试试吧！", msg_id)

    async def judge_guess(self, msg):
        """
        判断用户的猜测是否正确。
        用户猜测需要与歌曲的标题或别名有至少 20% 的连续字符匹配才被认为是正确的，空格不计入字符中。
        """
        if not msg:
            return False

        # 创建一个列表，包含歌曲标题和所有别名，并转换为小写，同时移除空格
        possible_answers = [self.current_song["title"].replace(" ", "").lower()] + [
            alias.replace(" ", "").lower()
            for alias in (self.alias_str or "").split("\n")
        ]
        logger.info("possible_answers: %s", possible_answers)

        # 将用户的猜测也转换为小写，并移除空格
        guess_lower = msg.replace(" ", "").lower()

        # 检查是否存在至少 20% 的连续字符匹配
        for answer in possible_answers:
            if self.get_max_match_length(guess_lower, answer) / len(answer) >= 0.2:
                return True
        return False

    def get_max_match_length(self, guess, answer):
        """
        获取 guess 在 answer 中的最长连续匹配长度。
        """
        max_length = 0
        for i in range(len(answer)):
            for j in range(i + 1, len(answer) + 1):
                if guess.find(answer[i:j]) != -1:
                    max_length = max(max_length, j - i)
        return max_length

    async def wait_for_guess(self):
        """
        等待玩家猜测，或直到时间结束。
        提供不同的提示信息。
        """
        await asyncio.sleep(20)  # 每 5 秒检查一次
        if self.game_active:
            await self.provide_hint(
                "genre or version or artist", msg_id=self.message.id
            )
            await asyncio.sleep(20)  # 每 5 秒检查一次

        if self.game_active:
            await self.provide_hint("difficulty level", msg_id=self.message.id)
            await asyncio.sleep(20)  # 每 5 秒检查一次

        if self.game_active:
            await self.provide_hint("cover image", msg_id=self.message.id)
            await asyncio.sleep(20)  # 每 5 秒检查一次

        if self.game_active:
            await self.end_game()

    async def provide_hint(self, hint_type, msg_id):
        """
        根据提示类型提供相应的提示。
        """
        if hint_type == "genre or version or artist":
            # 选择一个随机的提示信息：分类、版本或艺术家
            hint_options = [
                {"name": "分类", "value": self.current_song["genre"]},
                {
                    "name": "版本",
                    "value": get_version_name(self.current_song["version"]),
                },
                {"name": "艺术家", "value": self.current_song["artist"]},
                {"name": "BPM", "value": str(self.current_song["bpm"])},
            ]
            hint_info = random.choice(hint_options)
            await self.send_message(
                f"提示1: {hint_info['name']}为 {hint_info['value']}", msg_id
            )

        elif hint_type == "difficulty level":
            # 合并难度列表
            difficulties = []
            if self.current_song["difficulties"]["dx"]:
                difficulties.append(self.current_song["difficulties"]["dx"])
            if self.current_song["difficulties"]["standard"]:
                difficulties.append(self.current_song["difficulties"]["standard"])
            if difficulties:
                chosen_difficulty = random.choice(difficulties)
                # 随机选择提示难度等级或设计师
                hint_list = [
                    f"提示2: Master铺面难度等级为 {chosen_difficulty[3]['level']}",
                    f"提示2: Master铺面作者为 {chosen_difficulty[3]['note_designer']}",
                ]
                await self.send_message(random.choice(hint_list), msg_id)

        elif hint_type == "cover image":
            # 尝试获取封面图
            cover_path = await self.get_cover(120, 120)
            await self.send_message("提示3: 更大的曲绘", msg_id, image=cover_path)

    async def end_game(self):
        """
        结束游戏，并公布正确答案。
        """
        self.game_active = False
        assets = Assets.get_instance()
        cover = await assets.get(AssetType.COVER, self.current_song["id"])
        await self.send_message(
            f"正确答案是{self.current_song['title']}", self.message.id, image=cover
        )
        self.current_song = None

    @classmethod
    def is_game_active(cls, guild_id):
        """
        检查指定 guild 是否有游戏正在进行。
        """
        instance = cls._instances.get(guild_id)
        return instance.game_active if instance else False

    @staticmethod
    async def choice_song():
        """
        从曲目列表随机选择一首歌。
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                "https://maimai.lxns.net/api/v0/maimai/song/list", proxy=config.proxy
            ) as resp:
                if resp.status != 200:
                    return
                data = await resp.json()
                return random.choice(data.get("songs"))

    async def get_cover(self, length=70, width=70):
        """
        获取歌曲封面的一部分。如果95%的像素都是同一种颜色，则重新生成。
        """
        assets = Assets.get_instance()
        cover = await assets.get(AssetType.COVER, self.current_song["id"])
        img = Image.open(cover)

        # 尝试最多5次找到一个合适的裁剪区域
        for _ in range(5):
            x = random.randint(0, img.width - length)
            y = random.randint(0, img.height - width)
            crop_area = (x, y, x + length, y + width)
            cropped_img = img.crop(crop_area)

            # 计算每种颜色的像素数量
            color_counts = Counter(cropped_img.getdata())

            # 找出最常见颜色的像素数量
            most_common_color_count = color_counts.most_common(1)[0][1]

            # 检查是否满足95%的条件
            if most_common_color_count / (length * width) < 0.95:
                # 如果没有95%都是同一种颜色，则使用这个裁剪的图片
                temp_file = tempfile.mktemp(suffix=f"_{time.time()}_crop.png")
                cropped_img.save(temp_file)
                self.temp_files.append(temp_file)
                return temp_file

        # 如果经过5次尝试后还未找到合适的图片，返回最后一次尝试的结果
        temp_file = tempfile.mktemp(suffix=f"_{time.time()}_crop.png")
        cropped_img.save(temp_file)
        self.temp_files.append(temp_file)
        return temp_file
