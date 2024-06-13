import pathlib

import environ
from pydantic_settings import BaseSettings

BASE_DIR = pathlib.Path(__file__).parent.parent.parent
env = environ.Env()
environ.Env.read_env(str(BASE_DIR.joinpath(".env")))


class Settings(BaseSettings):
    token: str = env("TOKEN")
    music_max_length: int = env("MUSIC_MAX_LENGTH")


settings = Settings()
