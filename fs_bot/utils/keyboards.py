from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def start_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Подать заявку", callback_data="apply_request")
    builder.button(text="Информация", callback_data="start_info")

    builder.adjust(2)

    return builder.as_markup()

def default_inline(id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Мои группы", callback_data=f"groups_with_{id}")
    builder.button(text="Выход", callback_data=f"exit_with_{id}")

    builder.adjust(2)

    return builder.as_markup()

def admin_default_inline() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Добавить группу", callback_data="manager_add")
    builder.button(text="Удалить группу", callback_data="manager_delete")
    builder.button(text="Просмотреть все группы", callback_data="manager_all")

    builder.adjust(2, 1)

    return builder.as_markup()

def admin_apply_inline(id: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text="Да", callback_data=f"agree_request_with_{id}")
    builder.button(text="Нет", callback_data=f"decline_request_with_{id}")

    builder.adjust(2)

    return builder.as_markup()

def admin_groups_inline(groups: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for group in groups:
        builder.button(text=group, callback_data=f"manager_retrieve_group_{group}")

    builder.button(text="Назад к меню", callback_data="manager_start")

    builder.adjust(1)
    
    return builder.as_markup()

def admin_subjects_inline(group: str, subjects: list[str]) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for subject in subjects:
        builder.button(text=subject, callback_data=f"manager_{group}_retrieve_subject_{subject}")

    builder.button(text="Назад к группам", callback_data="manager_all")
    builder.adjust(1)

    return builder.as_markup()

def admin_subject_media(group: str, subject: str):
    builder = InlineKeyboardBuilder()
    builder.button(text='Добавить медиа файл', callback_data=f'manager_{group}_{subject}_add_media_')
    builder.button(text='Выход', callback_data=f'manager_retrieve_group_{group}')

    builder.adjust(2)
    
    return builder.as_markup()