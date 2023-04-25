import os
from fs_bot.core.settings import settings

def format_path(path: list[str]):
    root = settings.bots.project_archive
    full_path = os.path.join(root)
    for dir in path:
        os.path.join(full_path, dir)
    return full_path
    
