from pathlib import Path
from enum import Enum

import aiohttp
from botpy import logger


class AssetType(Enum):
    """
    AssetType
    枚举类型
    """

    COVER = "/assets/cover/"
    RANK = "/assets/rank/"
    BADGE = "/assets/badge/"
    COURSE_RANK = "/assets/course_rank/"
    CLASS_RANK = "/assets/class_rank/"
    RATING = "/assets/rating/"
    TROPHY = "/assets/trophy/"
    PLATE = "/assets/plate/"
    BG = "/assets/bg/"
    IMAGES = "/assets/images/"
    AVATAR = "/assets/avatar/"


class Assets:
    """
    资产类
    """

    _instance = None

    @classmethod
    def get_instance(
        cls, base_url: str = None, assets_folder: str = None, proxy: str = None
    ):
        """
        获取单例实例
        """
        if cls._instance is None:
            if base_url is None or assets_folder is None:
                raise ValueError("需要base_url和assets_folder来初始化")
            cls._instance = cls(base_url, assets_folder, proxy)
        return cls._instance

    def __init__(self, base_url: str, assets_folder: str, proxy: str = None) -> None:
        """
        初始化
        """
        if Assets._instance is not None:
            raise Exception("这是一个单例类，请使用 get_instance() 获取实例")
        self.base_url = base_url
        self.assets_folder = assets_folder
        self.proxy = proxy
        Assets._instance = self

    async def get(self, asset_type: AssetType, param_value) -> str:
        """
        获取资产
        """
        local_file_path = Path(
            self.assets_folder, asset_type.name.lower(), f"{param_value}.png"
        )
        if local_file_path.exists():
            return str(local_file_path)
        asset_url = f"{self.base_url}{asset_type.value}{param_value}"
        try:
            await self.download_file(asset_url, local_file_path, self.proxy)
        except aiohttp.ServerTimeoutError:
            logger.warning("下载文件超时：%s", asset_url)
        return str(local_file_path)

    def generate_assets_path(self, *paths: str) -> str:
        """
        获取资产路径
        """
        return str(Path(self.assets_folder, "basic", *paths))

    @staticmethod
    async def download_file(url: str, save_path: str, proxy=None):
        """
        从URL下载文件
        """
        logger.info("下载文件：%s", url)
        async with aiohttp.ClientSession(conn_timeout=5) as session:
            async with session.get(url, proxy=proxy) as response:
                if response.status != 200:
                    logger.warning("下载文件失败：%s", url)
                    return
                save_folder = Path(save_path).parent
                if not save_folder.exists():
                    save_folder.mkdir(parents=True)
                content = await response.read()
                with open(save_path, "wb") as file:
                    file.write(content)
                logger.info("从 %s 下载并保存文件到 %s", url, save_path)
