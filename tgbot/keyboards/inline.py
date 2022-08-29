from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardButton,InlineKeyboardBuilder
from aiogram import Bot, types


def confirm_buttons():
    help_buttons = InlineKeyboardBuilder()
    help_buttons.add(types.InlineKeyboardButton(
            text='Показати замовлення',
            callback_data='show'
        ))
    help_buttons.add(types.InlineKeyboardButton(
            text='Показати прибуток за тиждень',
            callback_data='earn'
        ))
    return help_buttons