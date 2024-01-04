import argparse
import os

import yaml
from botpy import logger


class AppConfig:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(AppConfig, cls).__new__(cls)
            # 在这里，可以执行类实例的初始化操作

        return cls._instance

    def __init__(self):
        self.qmsg_key = None
        self.bot_config = None
        self.static_config = None
        self.database_url = None
        self.debug = False
        self.loaded = False

    def load(self, config_path, env):
        if not self.loaded:
            try:
                with open(config_path, "r", encoding="utf-8") as file:
                    conf = yaml.safe_load(file)
                    env_config = conf.get(env, {})
                    self.bot_config = env_config.get("bot_config", {})
                    self.static_config = env_config.get("static_config", {})
                    self.database_url = env_config.get("database_url", "")
                    self.qmsg_key = env_config.get("qmsg_key", "")
                    self.debug = env_config.get("debug", False)
                    self.loaded = True
            except Exception as e:
                print(f"Error loading config: {e}")


def app_init():
    if not os.path.exists("log"):
        os.makedirs("log")

    parser = argparse.ArgumentParser(description="maimai bot")
    parser.add_argument(
        "-e",
        choices=["development", "production"],
        default="development",
        help="Set the environment (development/production)",
    )
    args = parser.parse_args()
    env = args.e
    logger.info(f"Environment: {env}")
    config.load("config.yaml", env)


# 创建配置实例
config = AppConfig()
app_init()
