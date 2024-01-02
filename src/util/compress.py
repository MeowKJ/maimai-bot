"""
This module provides functions for compressing PNG files asynchronously.
"""

import asyncio
import os
import subprocess


async def compress_png(fp, output, force=True, quality=None):
    force_command = "-f" if force else ""
    quality_command = ""

    if quality and isinstance(quality, int):
        quality_command = f"--quality {quality}"
    if quality and isinstance(quality, str):
        quality_command = f"--quality {quality}"

    command = f"pngquant {fp} --skip-if-larger {force_command} {quality_command} --output {output}"

    process = await asyncio.create_subprocess_shell(
        command, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
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
        raise subprocess.CalledProcessError(process.returncode, command)

    return compression_ratio
