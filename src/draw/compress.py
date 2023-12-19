import asyncio
import os

async def compress_png(fp, output, force=True, quality=None):
    """异步压缩函数.
    参数：
        fp: 文件名称
        output: 压缩后的文件名称
        force: 如果存在同名文件，是否覆盖
        quality: 压缩质量。 10-40，or 10
    """
    force_command = '-f' if force else ''
    quality_command = ''

    if quality and isinstance(quality, int):
        quality_command = f'--quality {quality}'
    if quality and isinstance(quality, str):
        quality_command = f'--quality {quality}'

    command = f'pngquant {fp} --skip-if-larger {force_command} {quality_command} --output {output}'

    process = await asyncio.create_subprocess_shell(
        command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # 等待命令执行完成
    _, _ = await process.communicate()

    # 获取原始图像大小
    original_size = os.path.getsize(fp)

    # 获取压缩后文件的大小
    compressed_size = os.path.getsize(output)

    # 计算压缩比
    compression_ratio = (1 - compressed_size / original_size) * 100
    # 检查命令是否成功执行
    if process.returncode != 0:
        raise Exception(f"pngquant 执行失败。返回码: {process.returncode}")

    return compression_ratio
