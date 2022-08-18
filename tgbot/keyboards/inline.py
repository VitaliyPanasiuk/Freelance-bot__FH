from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardButton,InlineKeyboardBuilder
from aiogram import Bot, types



def confirm_buttons():
    help_buttons = InlineKeyboardBuilder()
    help_buttons.add(types.InlineKeyboardButton(
            text='confirm',
            callback_data='confirm'
        ))
    help_buttons.add(types.InlineKeyboardButton(
            text='skip',
            callback_data='skip'
        ))
    return help_buttons