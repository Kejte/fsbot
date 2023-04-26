import asyncio
import os
import logging
from fs_bot.core.settings import settings
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from fs_bot.utils.commands import set_commands
from fs_bot.core.handlers import basic, manager
from fs_bot.utils.states import AddGroupState, AddMediaState


async def start_bot(bot: Bot):
    await set_commands(bot)
    try:
        os.mkdir(settings.bots.project_archive, mode=777)
    except FileExistsError:
        pass
    await bot.send_message(settings.bots.admin_id, text='Бот запущен!')

async def stop_bot(bot: Bot):
    await bot.send_message(settings.bots.admin_id, text='Бот выключен!')

async def load_bot():
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - [%(levelname)s] - %(name)s -'''
                               '(%(filename)s).%(funcName)s(%(lineno)d) - %(message)s'
                        )
    bot = Bot(token=settings.bots.bot_token, parse_mode='HTML')
    dp = Dispatcher()


    dp.startup.register(start_bot)
    dp.shutdown.register(stop_bot)
    dp.message.register(basic.drop_start, Command(commands='start'))
    dp.callback_query.register(basic.apply_request, F.data.contains("apply_request"))
    dp.callback_query.register(basic.agree_request, F.data.startswith("agree_request_with"))
    dp.callback_query.register(basic.decline_request, F.data.startswith("decline_request_with"))
    dp.callback_query.register(basic.groups, F.data.startswith("groups_with"))
    dp.callback_query.register(basic.exit, F.data.startswith("exit_with"))
    dp.callback_query.register(manager.start_admin, F.data.startswith("manager_start"))
    dp.callback_query.register(manager.add_group_start, F.data.startswith("manager_add"))
    dp.message.register(manager.add_group_title, AddGroupState.GET_TITLE)
    dp.message.register(manager.add_group_subject, AddGroupState.GET_SUBJECT)
    dp.message.register(manager.add_group_result, AddGroupState.GET_RESULT)
    dp.callback_query.register(manager.delete_group, F.data.startswith("manager_delete"))
    dp.callback_query.register(manager.all_groups, F.data.startswith("manager_all"))
    dp.callback_query.register(manager.retrieve_group, F.data.contains("retrieve_group"))
    dp.callback_query.register(manager.retrieve_group_subject, F.data.contains("retrieve_subject"))
    dp.callback_query.register(manager.get_subject_media, F.data.contains('add_media'))
    dp.message.register(manager.save_subject_media, AddMediaState.GET_MEDIA )
    
    

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()


def start():
    asyncio.run(load_bot())
