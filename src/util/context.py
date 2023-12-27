"""
Context for botpy
"""
import os

from botpy.ext.cog_yaml import read
from botpy import logging

context = {
    "assets_path": "./static/mai",
    "font_path": "./static/fonts",
    "en_font": "BungeeInline-Regular.ttf",
    "jp_font": "CusterMagic-Regular.ttf",
    "mix_font": "happy.ttf",
}

logger = logging.get_logger()
app_config = read("config.yaml")
