from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from fs_bot.utils import keyboards
from fs_bot.core.settings import settings

async def drop_start(message: Message, bot: Bot):
    if message.from_user.id == settings.bots.manager:
        await bot.send_message(settings.bots.manager, f"Приветствую, менеджер {message.from_user.full_name}! Выберите действие", reply_markup=keyboards.admin_default_inline())
        return
    await bot.send_message(message.from_user.id, f'Привет, выбери действие', reply_markup=keyboards.start_inline())

async def apply_request(callback: CallbackQuery, bot: Bot):
    try:
        await bot.send_message(settings.bots.manager, 
                           f"Поступил запрос от пользователя с никнеймом {callback.from_user.full_name}, продолжить?",
                           reply_markup=keyboards.admin_apply_inline(callback.from_user.id))
    except Exception:
        await bot.send_message(callback.from_user.id, "К сожалению, зарегистрироваться временно невозможно, попробуйте зайти позднее")
        return
    await bot.send_message(callback.from_user.id, "Нужно немного подождать, менеджер подтверждает запрос на вашу регистрацию")

async def agree_request(callback: CallbackQuery, bot: Bot):
    await bot.send_message(callback.data.split("_")[3], f"Вы успешно зарегистрированы, выберите действие", reply_markup=keyboards.default_inline())

async def decline_request(callback: CallbackQuery, bot: Bot):
    await bot.send_message(callback.data.split("_")[3], "К сожалению, ваш запрос отклонен. Подайте заявку позже")

async def groups(callback: CallbackQuery, bot: Bot):
    pass

async def exit(callback: CallbackQuery, bot: Bot):
    pass

