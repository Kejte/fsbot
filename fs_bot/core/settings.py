import sys
import os
from pathlib import Path
from environs import Env
from dataclasses import dataclass

@dataclass
class Bots:
    bot_token: str
    admin_id: int
    project_archive: str
    manager: int
    user_accessed_list: str


@dataclass
class Settings:
    bots: Bots



def get_settings(path: str):
    env = Env()
    env.read_env(path)

    return Settings(
        bots=Bots(
            bot_token=env.str('TOKEN'),
            admin_id=env.int('ADMIN_ID'),
            project_archive=os.path.join(Path(__file__).parent.parent, env.str("ARCHIVE")),
            manager = env.int("MANAGER"),
            user_accessed_list=os.path.join(Path(__file__).parent.parent, env.str("USER_ACCESSED_LIST"))+".txt"
        )
    )

settings = get_settings('input')
