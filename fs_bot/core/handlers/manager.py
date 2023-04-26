from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
import os
from fs_bot.core.settings import settings
from fs_bot.utils import keyboards, states
from fs_bot.core.service import manager


async def start_admin(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, "Выберите действие", reply_markup=keyboards.admin_default_inline())

async def add_group_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("Введите название группы")
    await state.set_state(states.AddGroupState.GET_TITLE)

async def add_group_title(message: Message, state: FSMContext):
    await state.update_data(title=message.text)

    await message.answer("Теперь укажите дисциплины через Enter\n"
                           "Например:" 
                           "\nPythonJunior"
                           "\nPythonMiddle"
                           "\n"
                           "p.s Если хотите указать дисциплины позже, напишите /cancel")
    await state.set_state(states.AddGroupState.GET_SUBJECT)

async def add_group_subject(message: Message, state: FSMContext):
    await state.update_data(members="Не указаны" if message.text=="/cancel" else message.text)
    await message.answer("Отлично! Теперь взглянем на новую группу...")

    context = await state.get_data()
    
    await message.answer("Данные группы верны?\n"
                         f"Название: {context['title']}\n"
                         f"Дисциплины: \n{context['members']}")

    await state.set_state(states.AddGroupState.GET_RESULT)

async def add_group_result(message: Message, state: FSMContext):
    if message.text.strip().lower() == "нет":
        await message.answer("Создание группы отменено, выберите дальнейшее действие", reply_markup=keyboards.admin_default_inline())
        return
    context = await state.get_data()
    if manager.create_group_dir(context['title'], context['members'].split("\n")):
        await message.answer("Группа и дисциплины созданы!", reply_markup=keyboards.admin_default_inline())
    else:
        await message.answer("Что-то пошло не так, обратитесь к системному администратору", reply_markup=keyboards.admin_default_inline())

async def all_groups(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    groups = [dir for dir in os.listdir(settings.bots.project_archive) if os.path.isdir(os.path.join(settings.bots.project_archive, dir))]
    await bot.send_message(callback.from_user.id, f"Выберите группу" if groups else "Групп не найдено", reply_markup=keyboards.admin_groups_inline(groups))

async def retrieve_group(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    group_dir = os.path.join(settings.bots.project_archive, callback.data.split("_")[3])
    subjects = os.listdir(group_dir)
    await bot.send_message(callback.from_user.id, "Выберите дисципдины" if subjects else "Дисциплины не добавлены в группу", 
                           reply_markup=keyboards.admin_subjects_inline(callback.data.split("_")[3], subjects))

async def retrieve_group_subject(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    group = callback.data.split("_")[1]
    subject = callback.data.split("_")[4]
    await bot.send_message(callback.from_user.id, 'Выберите действие',
                           reply_markup=keyboards.admin_subject_media(group, subject))

async def get_subject_media(callback: CallbackQuery, state: FSMContext):
    group = callback.data.split("_")[1]
    subject = callback.data.split("_")[2]
    await state.update_data(group=group, subject=subject)
    await callback.message.answer('Отправьте медиа файл')
    await state.set_state(states.AddMediaState.GET_MEDIA)
    

async def save_subject_media(message: Message, state: FSMContext, bot: Bot):
        context = await state.get_data()
        file = await bot.get_file(message.photo[-1].file_id)
        pathname = file.file_path.split("/")
        await bot.download_file(file.file_path, os.path.join(settings.bots.project_archive, context['group'], context['subject'], pathname[0], pathname[1]))
        await message.answer(f'Ваш файл успешно сохранен в директорию')
