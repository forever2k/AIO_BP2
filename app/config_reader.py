import configparser
from dataclasses import dataclass


@dataclass
class AskBot:
    test_group: int
    test: int
    me: str
    TOKEN: str
    PROJECT_NAME: str
    WEBHOOK_HOST: str
    WEBHOOK_PATH: str
    WEBHOOK_URL: str
    WEBAPP_HOST: str
    WEBAPP_PORT: str



@dataclass
class Config:
    ask_bot: AskBot


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    ask_bot = config["ask_bot"]

    return Config(
        tg_bot=AskBot(
            test_group=int(ask_bot["test_group"]),
            test=int(ask_bot["test"]),
            me=ask_bot["me"],
            TOKEN=ask_bot["TOKEN"],
            PROJECT_NAME=ask_bot["PROJECT_NAME"],
            WEBHOOK_HOST=ask_bot["WEBHOOK_HOST"],
            WEBHOOK_PATH=ask_bot["WEBHOOK_PATH"],
            WEBHOOK_URL=ask_bot["WEBHOOK_URL"],
            WEBAPP_HOST=ask_bot["WEBAPP_HOST"],
            WEBAPP_PORT=ask_bot["WEBAPP_PORT"],
        )
    )