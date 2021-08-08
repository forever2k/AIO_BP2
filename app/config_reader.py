import configparser
from dataclasses import dataclass


@dataclass
class AskBot:
    test_group: int
    test: int


@dataclass
class Config:
    ask_bot: AskBot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    ask_bot = config["ask_bot"]

    return Config(
        ask_bot=AskBot(
            test_group=int(ask_bot["test_group"]),
            test=int(ask_bot["test"]),
        )
    )