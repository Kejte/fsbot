from fs_bot.core.settings import settings

def add_user(user: int):
    return open(settings.bots.user_accessed_list, "a").write(f"{user},")

def get_users():
    users = [int(user) for user in open(settings.bots.user_accessed_list, "r").readline().split(",")[:-1]]
    return users