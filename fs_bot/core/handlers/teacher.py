from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from fs_bot.utils import keyboards
from fs_bot.core.settings import settings
import os
from aiogram.fsm.context import FSMContext
from fs_bot.utils import states

async def all_groups(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    groups = [dir for dir in os.listdir(settings.bots.project_archive) if os.path.isdir(os.path.join(settings.bots.project_archive, dir))]
    await bot.send_message(callback.from_user.id, f"Выберите группу" if groups else "Групп не найдено", reply_markup=keyboards.teacher_groups_inline(groups))

async def teacher_start(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    await bot.send_message(callback.from_user.id, 'Выберите действие', reply_markup=keyboards.teacher_default_inline())

async def all_groups(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    groups = [dir for dir in os.listdir(settings.bots.project_archive) if os.path.isdir(os.path.join(settings.bots.project_archive, dir))]
    await bot.send_message(callback.from_user.id, f"Выберите группу" if groups else "Групп не найдено", reply_markup=keyboards.teacher_groups_inline(groups))

async def retrieve_group(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    group_dir = os.path.join(settings.bots.project_archive, callback.data.split("_")[3])
    subjects = os.listdir(group_dir)
    await bot.send_message(callback.from_user.id, "Выберите дисципдины" if subjects else "Дисциплины не добавлены в группу", 
                           reply_markup=keyboards.teacher_subjects_inline(callback.data.split("_")[3], subjects))

async def retrieve_group_subject(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    group = callback.data.split("_")[1]
    subject = callback.data.split("_")[4]
    await bot.send_message(callback.from_user.id, 'Выберите действие',
                           reply_markup=keyboards.teacher_subject_media(group, subject))

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