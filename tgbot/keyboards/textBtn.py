from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardButton, InlineKeyboardBuilder
from aiogram import Bot, types


def typeBtn():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="курсова")
    )
    home_buttons.add(
        types.KeyboardButton(text="дипломна")
    )
    home_buttons.add(
        types.KeyboardButton(text="магістерська")
    )
    home_buttons.add(
        types.KeyboardButton(text="реферат")
    )
    home_buttons.adjust(2)
    return home_buttons