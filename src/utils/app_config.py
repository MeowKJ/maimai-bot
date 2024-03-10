"""
app_config.py - The configuration file for the app.
"""

import sys
import os
import yaml
from botpy import logger


class AppConfig:
    """ """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self.qmsg_key = None
        self.bot_config = None
        self.static_config = None
        self.database_url = None
        self.debug = False
        self.loaded = False

    def load(self, config_path):
        """
        Load the config file.

        Args:
            config_path: The path of the config file.
        """
        if not self.loaded:
            try:
                with open(config_path, "r", encoding="utf-8") as file:
                    conf = yaml.safe_load(file)
                    self.bot_config = conf.get("bot_config", {})
                    self.static_config = conf.get("static_config", {})
                    self.database_url = conf.get("database_url", "")
                    self.qmsg_key = conf.get("qmsg_key", "")
                    self.debug = conf.get("debug", False)
                    self.loaded = True
            except FileNotFoundError as e:
                print(f"Error loading config: {e}")
            except yaml.YAMLError as e:
                print(f"Error loading config: {e}")


def create_config_file(config_path):
    """
    Create the config file if it does not exist.

    Args:
        config_path: The path of the config file.

    """
    if not os.path.exists(config_path):
        default_config = {
            "bot_config": {
                "appid": "",
                "secret": "",
                "api_secret": "",
                "is_sandbox": False,
            },
            "static_config": {
                "assets_path": "./static/mai",
                "font_path": "./static/fonts",
                "en_font": "BungeeInline-Regular.ttf",
                "jp_font": "CusterMagic-Regular.ttf",
                "mix_font": "happy.ttf",
            },
            "database_url": "",
            "qmsg_key": "",
            "debug": False,
        }
        with open(config_path, "w", encoding="utf-8") as file:
            yaml.dump(default_config, file)


def app_init(config_path="config.yaml"):
    """
    Initialize the app.

    Args:
        config_path: The path of the config file.
    """
    if not os.path.exists("log"):
        os.makedirs("log")

    create_config_file(config_path)

    if not os.path.exists(config_path):
        logger.error("%s not found!", config_path)
        sys.exit(1)

    config.load(config_path)


# 创建配置实例
config = AppConfig()
app_init()
