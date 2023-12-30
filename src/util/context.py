"""
Context for botpy
"""
import asyncio
import argparse
import yaml
from botpy import logging


def load_config():
    parser = argparse.ArgumentParser(description="maimai bot")
    parser.add_argument(
        "-e",
        choices=["development", "production"],
        default="development",
        help="Set the environment (development/production)",
    )
    args = parser.parse_args()
    env = args.e
    with open("config.yaml", "r", encoding="utf-8") as file:
        conf = yaml.safe_load(file)
        return conf.get(env, {})


logger = logging.get_logger()
config = load_config()
bot_config = config.get("bot_config", {})


LOG_LEVEL = config.get("LOG_LEVEL", "INFO")

static_config = config.get("static_config", {})
UNLOCK_KEY = config.get("UNLOCK_KEY", "")
DATABASE_URL = config.get("DATABASE_URI", "")
