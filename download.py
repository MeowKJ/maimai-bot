import asyncio
from src.assets_generator.get_assets import Assets, AssetType
from src.utils.app_config import config


async def download_asset(Assets_instance, asset_type, asset_number, semaphore):
    async with semaphore:
        await Assets_instance.get(asset_type, asset_number)


async def main():
    base_url = config.base_url
    assets_folder = config.static_config["assets_path"]

    Assets_instance = Assets(base_url=base_url, assets_folder=assets_folder)

    semaphore = asyncio.Semaphore(100)  # Limiting concurrent downloads to 10

    tasks = []
    for i in range(1, 20001):
        task = download_asset(Assets_instance, AssetType.COVER, i, semaphore)
        tasks.append(task)

    await asyncio.gather(*tasks)


if __name__ == "__main__":
    asyncio.run(main())
