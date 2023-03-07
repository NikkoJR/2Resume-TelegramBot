from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Text
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from config import TOKEN
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from buttons import keyboard_notes, keyboard_simple_notes, keyboard_in, keyboard_menu, keyboard_to_continue
import asyncio
import sqlite3




# Connect to bot in TG
bot: Bot = Bot(token=TOKEN)
dp: Dispatcher = Dispatcher()


#lists of user and his id to sing up / log in process
authorization_logs: dict = {'id_log': False,
                          'id_sing': False,
                          'authorization_id': False}

user_info: dict = {'table': ''}

work_with_notes: dict = {'add_notes_id': False,
                         'add_datenotes_id': False,
                         'wait_time': False,
                         'wait_number_of_note': False}


#Base of date
bd = sqlite3.connect('LDLN.bd')
cur = bd.cursor()

bd.execute('CREATE TABLE IF NOT EXISTS {}(login TEXT, password TEXT)'.format('users'))
bd.commit()


print('Bot "LDLNnotes v.01" is ON')





def table_exists(table_name):
    cur.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
    return cur.fetchone() is not None




#hendlers to commands

@dp.message(CommandStart())
async def start_process(message: Message):
    await message.answer("Привет. Я бот, создан командой LDLN.\nДля начала работы с заметками нужно зарезервировать таблицу / подключится к ней.\n\nДля авторизации или создания таблицы - /log\n\nЕсли у вас возникнут проблемы или вопросы - /help\nУзнать информацию о нас - /info")


#
#
#
#


@dp.message(Text(text='/help'))
async def help_process(message: Message):
    await message.answer('Если у вас возникли трудности - обратитесь к администратору (@n1kkostyle)')

@dp.message(Text(text='/info'))
async def help_process(message: Message):
    await message.answer('Бот создан командой LDLN.\nИспользуя бота вы сможете безопасно сохранять свои данные.\nПочему он удобнее обычных заметок?\n• Добавление заметок в 2 клика.\n• Безопасное хранение данных.\n• Удобное взаимодействие с заметками.')
    chat_id = message.from_user.id
    photo_url = 'https://sun9-20.userapi.com/impg/PNWUyscS_YFxpxZ39GYciw7ORDIp_5f2kQJZfw/bKFI5uwco9c.jpg?size=1024x1024&quality=95&sign=6d3a41795e2fcc3cf4f3711be5b33ac6&c_uniq_tag=n4ot2IgNONhy4kmc5BXi4ErKJDtTnpleY00prcTICr8&type=album'
    await bot.send_photo(chat_id, photo_url)


#
#
#


@dp.message(Text(text='/log'))
async def log_process(message: Message):
    await message.answer('У вас уже есть таблица или же вы хотите создать новую?', reply_markup=keyboard_in)



#Hendlers to log in and sing up



#process starting after command "sing up"
@dp.message(Text(text='Создать новую таблицу'))
async def sing_up(message: Message):
    await message.answer('Введите название желаемой таблицы:')
    await message.answer('P.S: Вводите название таблицы маленькими')
    authorization_logs['id_sing'] = True



@dp.message(lambda x: x.text and authorization_logs['id_sing'] == True)
async def process_sing_up_login(message: Message):
    table_name = message.text

    try:
        bd.execute('CREATE TABLE {}(simple_notes TEXT, src_notes TEXT, dates_notes TEXT, id INT AUTO_INCREMENT PRIMARY KEY)'.format(table_name))
        bd.commit()

        await message.answer('Таблица успешно создана.')
        await message.answer('Хотите авторизоваться?', reply_markup=keyboard_in)
        authorization_logs['id_sing'] = False

    except:
        await message.answer('Ошибка при создании таблицы!\nВозможно таблица с таким названием уже существует.')
        await message.answer('Попробуйте еще раз.', reply_markup=keyboard_in)
        authorization_logs['id_sing'] = False


#


#process starting after command "log in"
@dp.message(Text(text='Продолжить работу в старой таблице'))
async def login_in(message: Message):
    await message.answer('Введите логин (название таблицы):')
    authorization_logs['id_log'] = True



@dp.message(lambda x: x.text and authorization_logs['id_log'] == True)
async def process_login(message: Message):
    table_name = message.text

    try:

        if table_exists(table_name):
            authorization_logs['id_log'] = False
            authorization_logs['authorization_id'] = True
            await message.answer('Вы успешно авторизовались.')
            await message.answer('Нажмите "Управление заметками" - для взаимодействия с вашими заметками.\n\nНажмите "В меню" - для возвращения в меню.', reply_markup=keyboard_notes)
            user_info['table'] = table_name

        else:
            await message.answer('Таблица с таким названием не найдена!\nПопробуйте еще раз.', reply_markup=keyboard_in)
            authorization_logs['id_log'] = False

    except:

        await message.answer('Произошла ошибка при выполнении запроса!')
        authorization_logs['id_log'] = False


#
#

@dp.message(Text(text='Управление заметками'))
async def simple_notes(message: Message):

    if authorization_logs['authorization_id'] == True:
        await message.answer('Вы находитесь в стандартных заметках.\nВыберите нужный вам вариант:', reply_markup=keyboard_simple_notes)
        await message.answer('Нажмите "Все заметки" - чтобы просмотреть все добавленные вами простые заметки.\n\nНажмите "Выбрать нужную заметку" - чтобы просмотреть последнюю добавленную вами простую заметку.')
        await message.answer('Нажмите "Добавить заметку" - для добавления заметки.\n\nНажмите "Последняя заметка" - чтобы просмотреть последнюю добавленную вами простую заметку.\n\nНажмите "В меню" - для возвращения в меню.')

    elif authorization_logs['authorization_id'] == False:
        await message.answer('Вы не авторизовались!')


#


@dp.message(Text(text='Все заметки'))
async def simple_notes(message: Message):
    idS = 1
    listd = []
    table_name = user_info['table']

    if authorization_logs['authorization_id'] == True:

        while True:
            all_simple_notes = cur.execute(f'SELECT simple_notes FROM {table_name} WHERE rowid=?', (idS,)).fetchone()
            all_simple_notes = str(all_simple_notes)

            for i in all_simple_notes:
                if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                    all_simple_notes = all_simple_notes.replace(i, '')

            if all_simple_notes != 'None':
                listd.append(all_simple_notes)
                idS += 1

            elif all_simple_notes == 'None':
                print('Спизжено')
                await message.answer('Все заметки начиная сначала: ')

                for i in range(0, len(listd)):

                    message_from_list = listd[i]

                    await message.answer(message_from_list)

                await message.answer('Процесс остановлен.', reply_markup=keyboard_simple_notes)

                return False

    elif authorization_logs['authorization_id'] == False:
        await message.answer('Вы не авторизовались!')


#


@dp.message(Text(text='Выбрать нужную заметку'))
async def process_choice_note(message: Message):
    idS = 1
    listd = []
    table_name = user_info['table']

    if authorization_logs['authorization_id'] == True:

        while True:
            all_simple_notes = cur.execute(f'SELECT simple_notes FROM {table_name} WHERE rowid=?', (idS,)).fetchone()
            all_simple_notes = str(all_simple_notes)

            if all_simple_notes != 'None':
                listd.append(all_simple_notes)
                idS += 1

            elif all_simple_notes == 'None':
                await message.answer(f'Общее количество заметок - {len(listd)}. Выберите нужную: (Вводите число в чат)')

                work_with_notes['wait_number_of_note'] = True

                return False


#


@dp.message(lambda x: x.text and work_with_notes['wait_number_of_note'] == True and x.text.isdigit())
async def process_add_note(message: Message):
    work_with_notes['wait_number_of_note'] = False

    user_choice = message.text
    table_name = user_info['table']

    special_note = cur.execute(f'SELECT simple_notes FROM {table_name} WHERE rowid=?', (user_choice,)).fetchone()
    special_note = str(special_note)

    for i in special_note:
        if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
            special_note = special_note.replace(i, '')

    await message.answer(f'Заметка: {special_note}')
    await message.answer('Процесс остановлен.', reply_markup=keyboard_simple_notes)


#


@dp.message(Text(text='Добавить заметку'))
async def simple_notes(message: Message):

    if authorization_logs['authorization_id'] == True:
        await message.answer('Напишите текст заметки:')
        await message.answer('P.S: Не выходите за рамки одной строки. Пример - Купить: молоко, бананы.')
        work_with_notes['add_notes_id'] = True

    elif authorization_logs['authorization_id'] == False:
        await message.answer('Вы не авторизовались!')


@dp.message(lambda x: x.text and work_with_notes['add_notes_id'] == True)
async def process_add_note(message: Message):
    user_text = message.text
    table_name = user_info['table']

    cur.execute(f'INSERT INTO {table_name} (simple_notes) VALUES (?)', (user_text,))
    bd.commit()

    work_with_notes['add_notes_id'] = False
    work_with_notes['wait_time'] = True

    await message.answer('Текст успешно добавлен в таблицу.')
    await message.answer('Вы хотите продолжить?', reply_markup=keyboard_to_continue)


#


@dp.message(Text(text='Последняя заметка'))
async def simple_notes(message: Message):

    if authorization_logs['authorization_id'] == True:

        table_name = user_info['table']
        idS = 1
        listd = []

        while True:
            all_simple_notes = cur.execute(f'SELECT simple_notes FROM {table_name} WHERE rowid=?', (idS,)).fetchone()
            all_simple_notes = str(all_simple_notes)

            for i in all_simple_notes:
                if i == '(' or i == ')' or i == ',' or i == "'" or i == "[" or i == "]":
                    all_simple_notes = all_simple_notes.replace(i, '')

            if all_simple_notes != 'None':
                listd.append(all_simple_notes)
                idS += 1

            elif all_simple_notes == 'None':
                print('Спизжено')

                await message.answer(f'Последняя заметка - {listd[len(listd) - 1]}')
                await message.answer('Процесс остановлен.', reply_markup=keyboard_simple_notes)

                return False

    elif authorization_logs['authorization_id'] == False:
        await message.answer('Вы не авторизовались!')


#


@dp.message(Text(text='В меню'))
async def simple_notes(message: Message):
    await message.answer('Возвращение в меню:', reply_markup=keyboard_menu)


#
#
#
#


#Process after add new notes
@dp.message(Text(text='Да'))
async def simple_notes(message: Message):

    if work_with_notes['wait_time'] == True:
        work_with_notes['add_notes_id'] = True
        await message.answer('Продолжайте добавлять.')

    elif work_with_notes['wait_time'] == False:
        await message.answer("Я не могу работать с командами, для которых не предназначен")


@dp.message(Text(text='Нет'))
async def simple_notes(message: Message):

    if work_with_notes['wait_time'] == True:
        await message.answer('Процесс остановлен.', reply_markup=keyboard_simple_notes)

    elif work_with_notes['wait_time'] == False:
        await message.answer("Я не могу работать с командами, для которых не предназначен")


#Menu command
@dp.message(Text(text='Работа с заметками'))
async def simple_notes(message: Message):

    if authorization_logs['authorization_id'] == True:
        await message.answer('Нажмите "Управление заметками" - для взаимодействия с вашими заметками.\n\nНажмите "Назад в меню" - для возвращения в меню.', reply_markup=keyboard_simple_notes)


#Command to stop process
@dp.message(Text(text='/stop'))
async def simple_notes(message: Message):
    authorization_logs['id_log'] = False
    authorization_logs['id_sing'] = False
    work_with_notes['add_notes_id'] = False
    await message.answer('Процесс остановлен..')
    await message.answer('Система перезапущена.')
    await message.answer('Вы находитесь в меню:', reply_markup=keyboard_menu)


#Message to unknown commands or messages
@dp.message(lambda x: x.text)
async def process_login(message: Message):
    await message.answer("Я не могу работать с командами, для которых не предназначен")


if __name__ == '__main__':
    dp.run_polling(bot)

if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

