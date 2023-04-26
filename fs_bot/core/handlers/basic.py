from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from fs_bot.utils import keyboards
from fs_bot.core.settings import settings
from fs_bot.core.service import basic

async def drop_start(message: Message, bot: Bot):
    users = basic.get_users()
    if message.from_user.id == settings.bots.manager:
        await bot.send_message(settings.bots.manager, 
                               f"Приветствую, менеджер {message.from_user.full_name}!"
                               "Выберите действие", 
                               reply_markup=keyboards.admin_default_inline())
        return
    elif message.from_user.id in users:
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы, выберите действие", reply_markup=keyboards.teacher_default_inline())
        return
    await bot.send_message(message.from_user.id, f'Привет, выбери действие', reply_markup=keyboards.start_inline())

async def apply_request(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    try:
        await bot.send_message(settings.bots.manager, 
                           f"Поступил запрос от пользователя с никнеймом {callback.from_user.full_name}, продолжить?",
                           reply_markup=keyboards.admin_apply_inline(callback.from_user.id))
    except Exception:
        await bot.send_message(callback.from_user.id, "К сожалению, зарегистрироваться временно невозможно, попробуйте зайти позднее")
        return
    await bot.send_message(callback.from_user.id, "Нужно немного подождать, менеджер подтверждает запрос на вашу регистрацию")

async def agree_request(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    basic.add_user(callback.data.split("_")[3])
    await bot.send_message(callback.data.split("_")[3], f"Вы успешно зарегистрированы, выберите действие", reply_markup=keyboards.teacher_default_inline())

async def decline_request(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await bot.send_message(callback.data.split("_")[3], "К сожалению, ваш запрос отклонен. Подайте заявку позже")
