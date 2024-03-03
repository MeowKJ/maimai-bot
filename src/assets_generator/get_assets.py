import os
import aiohttp
from enum import Enum


class AssetType(Enum):
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
        if asset_type == AssetType.COVER:
            if isinstance(param_value, (int)) and param_value > 10000:
                param_value = param_value % 10000
        # 定义本地文件路径
        local_file_path = os.path.join(
            self.assets_folder, asset_type.name, str(param_value)
        )

        # 检查资产是否存在于本地
        if os.path.exists(local_file_path):
            return local_file_path

        # 如果本地不存在资产，则下载
        asset_url = f"{self.base_url}{asset_type.value}/{param_value}"
        await self.download_file(asset_url, local_file_path)

        return local_file_path

    @staticmethod
    async def download_file(url: str, save_path: str):
        """
        从URL下载文件
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    raise ValueError(f"请求失败，状态码为 {response.status}")

                # 读取文件内容
                content = await response.read()

                # 将内容保存到文件中
                with open(save_path, "wb") as file:
                    file.write(content)

                print(f"从 {url} 下载并保存文件到 {save_path}")
