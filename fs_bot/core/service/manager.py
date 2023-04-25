import os
from fs_bot.core.settings import settings
from fs_bot.utils import funcs


def create_group_dir(group: str, students: list[str]) -> bool:
    new_dir = os.path.join(settings.bots.project_archive, group)
    try:
        os.mkdir(new_dir)
        return _create_student_dirs(new_dir, students)
    except FileExistsError:
        return _create_student_dirs(new_dir, students)
    except Exception:
        return False
    


def _create_student_dirs(group: str, students: list[str]) -> bool:
    try:
        map(lambda s: os.mkdir(os.path.join(settings.bots.project_archive, group, s)), students)
    except Exception:
        return False
    return True

def get_student_dir(group: str, student: str) -> list[str]:
    dir = os.path.join(settings.bots.project_archive, group, student)
    return [subject for subject in os.listdir(dir) if os.path.isdir(os.path.join(dir, subject))]

def create_subject_dirs(group: str, student: str, subjects: list[str]) -> bool:
    try:
        map(lambda s: os.mkdir(funcs.format_path([group, student, s])), subjects)
    except Exception:
        return False
    return True