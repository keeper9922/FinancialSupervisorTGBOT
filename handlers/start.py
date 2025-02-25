import datetime

from aiogram import Router
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.types import Message, ChatMemberUpdated
from create_bot import database, translation

start_router = Router()
money_router = Router()

@start_router.message(CommandStart())
async def cmd_start(message: Message):
    try:
        await database.add_user(message.from_user.id)
    except Exception as error:
        print(error)
    await message.answer(translation.command_translation('start')['success'])

# При приглашении в группу
# @start_router.my_chat_member()
# async def on_join_chat(event: ChatMemberUpdated):
#     print(event.chat.id)
#     await event.answer(f"Простите, данный бот пока что функционирует только в личных сообщениях")

@start_router.message(Command('menu'))
async def cmd_menu(message: Message):
    await message.answer(translation.command_translation('menu')['success'] % (str(datetime.date.today()), str(datetime.date.today()-datetime.timedelta(days=1)), str(datetime.date.today())), parse_mode='Markdown')

@money_router.message(Command('print'))
async def cmd_print(message: Message, command: CommandObject):
    try:
        args = command.args
        print(args)
        if args:
            result = await database.get_total_finances_by_date(message.from_user.id, args)
        else:
            result = await database.get_total_finances_by_date(message.from_user.id)
        await message.answer(translation.command_translation('print')['success'] % result)
    except IndexError:
        await message.answer(translation.command_translation('print')['success'] % 0)
    except Exception as e:
        print(e)
        await message.answer(translation.command_translation('print')['error'])

@money_router.message(Command('print_total'))
async def cmd_print(message: Message):
    try:
        result = await database.get_total_finances(message.from_user.id)
        await message.answer(translation.command_translation('print_total')['success'] % result)
    except IndexError:
        await message.answer(translation.command_translation('print_total')['success'] % 0)
    except Exception as e:
        print(e)
        await message.answer(translation.command_translation('print_total')['error'])

@money_router.message(Command('print_period'))
async def cmd_print(message: Message, command: CommandObject):
    try:
        args = command.args.split(' ')
        print(args)
        result = await database.get_total_finances_period(message.from_user.id, args[0], args[1])
        await message.answer(translation.command_translation('print_period')['success'] % result)
    except IndexError:
        await message.answer(translation.command_translation('print_period')['success'] % 0)
    except Exception as e:
        print(e)
        await message.answer(translation.command_translation('print_period')['error'] % (str(datetime.date.today()-datetime.timedelta(days=1)), str(datetime.date.today())))

@money_router.message(Command('periods'))
async def cmd_print(message: Message):
    try:
        result = await database.get_finances(message.from_user.id)
        formated_result = "Вывод периодов:\n"
        for i in range(len(result)):
            formated_result += translation.command_translation('periods')['success'] % (i, result[i][0], str(result[i][1]))
        await message.answer(formated_result, parse_mode= "Markdown")
    except IndexError:
        await message.answer(translation.command_translation('periods')['success'] % (0, 0, datetime.date.today()))
    except Exception as error:
        print(error)
        await message.answer(translation.command_translation('periods')['error'])

@money_router.message()
async def dm_message(message: Message):
    try:
        number = int(message.text)
        await database.add_finances(message.from_user.id, number)
        await message.answer(translation.command_translation('.message')['success'])
    except ValueError or TypeError:
        await message.answer(translation.command_translation('.message')['error'])



# @start_router.message(Command('start_2'))
# async def cmd_start_2(message: Message):
#     await message.answer('Запуск сообщения по команде /start_2 используя фильтр Command()')
#
# @start_router.message(F.text == '/start_3')
# async def cmd_start_3(message: Message):
#     await message.answer('Запуск сообщения по команде /start_3 используя магический фильтр F.text!')