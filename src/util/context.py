"""
Context for botpy
"""

from botpy import logging

context = {
    "assets_path": "./static/mai",
    "font_path": "./static/fonts",
    "en_font": "BungeeInline-Regular.ttf",
    "jp_font": "CusterMagic-Regular.ttf",
    "mix_font": "happy.ttf",
}

_log = logging.get_logger()
