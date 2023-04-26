import os
from fs_bot.core.settings import settings


def create_group_dir(group: str, subject: list[str]) -> bool:
    new_dir = os.path.join(settings.bots.project_archive, group)
    try:
        os.mkdir(new_dir, mode=777)
        return _create_subjects_dirs(group, subject)
    except FileExistsError:
        return _create_subjects_dirs(group, subject)
    except Exception:
        return False
    


def _create_subjects_dirs(group: str, subjects: list[str]) -> bool:
    try:
        for subject in subjects:
            os.mkdir(os.path.join(settings.bots.project_archive, group, subject), mode=777)
            os.mkdir(os.path.join(settings.bots.project_archive, group, subject, "photos"), mode=777)
            os.mkdir(os.path.join(settings.bots.project_archive, group, subject, "videos"), mode=777)
    except Exception:
        return False
    return True

def get_subject_dir(group: str, subject: str) -> list[str]:
    dir = os.path.join(settings.bots.project_archive, group, subject)
    return [subject for subject in os.listdir(dir) if os.path.isdir(os.path.join(dir, subject))]

