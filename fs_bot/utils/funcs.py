import os
from time import ctime
from fs_bot.core.settings import settings

def format_path(path: list[str]):
    root = settings.bots.project_archive
    full_path = os.path.join(root)
    for dir in path:
        os.path.join(full_path, dir)
    return full_path

# bubble sort by time algorithm
def sorted_by_time(dirs: list[str]):
    for i in range(len(dirs)):
        for j in range(0, len(dirs)-i-1):
            if ctime(os.path.getctime(os.path.join(settings.project_archive, dirs[j]))) > ctime(os.path.getctime(dirs[j+1])):
                temp = dirs[j]
                dirs[j] = dirs[j+1]
                dirs[j+1]=temp
    return dirs