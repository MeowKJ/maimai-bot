"""
This module provides functions for compressing PNG files asynchronously.
"""

import asyncio
import os
import subprocess


async def compress_png(fp, output, force=True, quality=None):
    """
    Compresses a PNG file asynchronously.

    Args:
        fp (str): The file path of the original PNG file.
        output (str): The file path for the compressed PNG file.
        force (bool, optional): Whether to force compression. Defaults to True.
        quality (int or str, optional): Compression quality parameter. Defaults to None.

    Returns:
        float: Compression ratio percentage.
    """
    if not os.path.exists(fp):
        raise FileNotFoundError(f"File not found: {fp}")

    force_command = "-f" if force else ""
    quality_command = ""

    if quality and isinstance(quality, int):
        quality_command = f"--quality {quality}"
    if quality and isinstance(quality, str):
        quality_command = f"--quality {quality}"

    command = (
        f"pngquant {fp} "
        f"--skip-if-larger {force_command} "
        f"{quality_command} "
        f"--output {output}"
    )

    try:
        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )
        _, _ = await process.communicate()

        # 获取原始图像大小
        original_size = os.path.getsize(fp)

        # 获取压缩后文件的大小
        compressed_size = os.path.getsize(output)

        # 计算压缩比
        compression_ratio = (1 - compressed_size / original_size) * 100
        # 检查命令是否成功执行
        if process.returncode != 0:
            raise subprocess.CalledProcessError(process.returncode, command)

        return compression_ratio
        # 剩下的代码...
    except asyncio.CancelledError as exc:
        # 处理异步任务被取消的情况
        raise exc from None
    except Exception as e:
        # 处理其他异常
        raise RuntimeError(f"An error occurred: {e}") from e
