"Assets Generator"
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

    def __init__(self, base_url: str, assets_folder: str) -> None:
        """
        初始化
        """
        self.base_url = base_url
        self.assets_folder = assets_folder

    async def get(self, asset_type: AssetType, param_value) -> str:
        """
        获取资产
        """
        # 定义本地文件路径
        local_file_path = Path(
            self.assets_folder, asset_type.name.lower(), str(param_value) + ".png"
        )

        # 检查资产是否存在于本地
        if local_file_path.exists():
            return str(local_file_path)

        # 如果本地不存在资产，则下载
        asset_url = f"{self.base_url}{asset_type.value}{param_value}"
        await self.download_file(asset_url, local_file_path)

        return local_file_path

    def generate_assets_path(self, *paths: str) -> str:
        """
        获取资产路径
        """
        return str(Path(self.assets_folder, "basic", *paths))

    @staticmethod
    async def download_file(url: str, save_path: str):
        """
        从URL下载文件
        """
        logger.info("下载文件：%s", url)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"请求失败，状态码为 {response.status}")
                # 确保保存文件的文件夹存在
                save_folder = Path(save_path).parent
                if not save_folder.exists():
                    save_folder.mkdir(parents=True)
                # 读取文件内容
                content = await response.read()
                # 将内容保存到文件中
                with open(save_path, "wb") as file:
                    file.write(content)

                logger.info("从 %s 下载并保存文件到 %s", url, save_path)
