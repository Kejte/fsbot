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

    await message.answer("Теперь укажите студентов через Enter\n"
                           "Например:" 
                           "\nВаняВасильев"
                           "\nМашаЗавъявлова"
                           "\n"
                           "p.s Если хотите указать студентов позже, напишите /cancel")
    await state.set_state(states.AddGroupState.GET_MEMBERS)

async def add_group_members(message: Message, state: FSMContext):
    await state.update_data(members="Не указаны" if message.text=="/cancel" else message.text)
    await message.answer("Отлично! Теперь взглянем на новую группу...")

    context = await state.get_data()
    
    await message.answer("Данные группы верны?\n"
                         f"Название: {context['title']}\n"
                         f"Студенты: \n{context['members']}")

    await state.set_state(states.AddGroupState.GET_RESULT)

async def add_group_result(message: Message, state: FSMContext):
    if message.text.strip().lower() == "нет":
        await message.answer("Создание группы отменено, выберите дальнейшее действие", reply_markup=keyboards.admin_default_inline())
        return
    context = await state.get_data()
    if manager.create_group_dir(context['title'], context['members'].split("\n")):
        await message.answer("Группа и студенты созданы!")
    else:
        await message.answer("Что-то пошло не так, обратитесь к системному администратору")

async def delete_group(callback: CallbackQuery, bot: Bot):
    pass

async def all_groups(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    groups = [dir for dir in os.listdir(settings.bots.project_archive) if os.path.isdir(os.path.join(settings.bots.project_archive, dir))]
    await bot.send_message(callback.from_user.id, f"Выберите группу" if groups else "Групп не найдено", reply_markup=keyboards.admin_groups_inline(groups))

async def retrieve_group(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    group_dir = os.path.join(settings.bots.project_archive, callback.data.split("_")[3])
    students = os.listdir(group_dir)
    await bot.send_message(callback.from_user.id, "Выберите студента" if students else "Студенты не добавлены в группу", 
                           reply_markup=keyboards.admin_students_inline(callback.data.split("_")[3], students))


async def retrieve_group_student(callback: CallbackQuery, bot: Bot):
    await callback.message.delete()
    group = callback.data.split("_")[1]
    student = callback.data.split("_")[4]
    subjects = manager.get_student_dir(group, student)
    await bot.send_message(callback.from_user.id, 'Выберите предмет студента' if subjects else "Предметов не найдено",
                           reply_markup=keyboards.admin_student_subjects(group, student, subjects))
    
async def add_student_subject_start(callback: CallbackQuery, state: FSMContext):
    await callback.message.delete()
    await callback.message.answer(
        "Введите названия дисциплин в формате: \n"
        "PythonJunior\n"
        "PythonMiddle\n"
        "и так далее..."
        )
    group = callback.data.split("_")[1]
    student = callback.data.split("_")[2]
    await state.update_data(group=group, student=student)
    await state.set_state(states.AddSubjectsState.GET_SUBJECTS)

async def add_student_subject_end(message: Message, state: FSMContext):
    context = await state.get_data()
    group = context['group']
    student = context['student']
    subjects = message.text.split("\n")
    if manager.create_subject_dirs(context['group'], context['student'], message.text):
        await message.answer("Дисциплины для студента созданы успешно!", 
                             reply_markup=keyboards.admin_student_subjects(group, student, subjects))
    else:
        await message.answer("Произошла ошибка, обратитесь к системному администратору")

async def retrieve_group_student_subject(callback: CallbackQuery, bot: Bot):
    pass

async def retrieve_group_student_subject_photo(callback: CallbackQuery, bot: Bot):
    pass

async def retrieve_group_student_subject_video(callback: CallbackQuery, bot: Bot):
    pass

async def save_student_media(message: Message, bot: Bot):
        file = None
        match message:
            case message.photo:
                file = await bot.get_file(message.photo[-1].file_id)
            case message.video:
                file = await bot.get_file(message.video.file_id)
            case _:
                await bot.send_message(message.chat.id, 'В данный момент мы не можем сохранить данный тип файла')
                return
        await bot.download_file(file.file_path, )
        await message.answer(f'Ваш файл успешно сохранен в директорию')




