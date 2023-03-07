from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart, Text
from aiogram.types import (KeyboardButton, Message, ReplyKeyboardMarkup,
                           ReplyKeyboardRemove)
from config import TOKEN
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonPollType
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
import asyncio
import sqlite3


#main notes buttons
button_to_simple_notes: KeyboardButton = KeyboardButton(text='Управление заметками')
button_to_back: KeyboardButton = KeyboardButton(text='В меню')


#create notes keyboards
keyboard_notes: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_to_simple_notes], [button_to_back]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

#
#
#
#


#Main simple notes buttons
button_show_all_simple_notes: KeyboardButton = KeyboardButton(text='Все заметки')
button_show_special_note: KeyboardButton = KeyboardButton(text='Выбрать нужную заметку')
button_add_to_simple_notes: KeyboardButton = KeyboardButton(text='Добавить заметку')
button_show_last_note: KeyboardButton = KeyboardButton(text='Последняя заметка')
button_return_back_menu: KeyboardButton = KeyboardButton(text='В меню')

#Create simple notes keyboards
keyboard_simple_notes: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_show_all_simple_notes], [button_show_special_note], [button_add_to_simple_notes], [button_show_last_note], [button_return_back_menu]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)


#
#
#


#All notes in simple notes
button_to_log_in: KeyboardButton = KeyboardButton(text='Продолжить работу в старой таблице')
button_to_sing_up: KeyboardButton = KeyboardButton(text='Создать новую таблицу')


keyboard_in: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_to_log_in], [button_to_sing_up]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)


#
#
#


#Buttons after stop command
button_to_work_with_notes: KeyboardButton = KeyboardButton(text='Работа с заметками')
button_to_log: KeyboardButton = KeyboardButton(text='/log')

keyboard_menu: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[button_to_work_with_notes], [button_to_log]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)


#
#
#

#Buttons to ask to stop add notes or no
yes_button: KeyboardButton = KeyboardButton(text='Да')
no_button: KeyboardButton = KeyboardButton(text='Нет')

keyboard_to_continue: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
                                    keyboard=[[yes_button], [no_button]],
                                    resize_keyboard=True,
                                    one_time_keyboard=True)

