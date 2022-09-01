from aiogram.utils.keyboard import ReplyKeyboardBuilder,InlineKeyboardButton,InlineKeyboardBuilder
from aiogram import Bot, types


def confirm_buttons():
    help_buttons = InlineKeyboardBuilder()
    help_buttons.add(types.InlineKeyboardButton(
            text='📚Актуальне',
            callback_data='show'
        ))
    help_buttons.add(types.InlineKeyboardButton(
            text='💰Виплати',
            callback_data='earn'
        ))
    return help_buttons

def adm_buttons():
    help_buttons = InlineKeyboardBuilder()
    help_buttons.row(types.InlineKeyboardButton(
            text='Рассылка',
            callback_data='mailing'
        ))
    help_buttons.row(types.InlineKeyboardButton(
            text='Добавить автора',
            callback_data='addauthor'
        ))
    help_buttons.row(types.InlineKeyboardButton(
            text='Добавить автора в аукцион',
            callback_data='addauthorprivate'
        ))
    help_buttons.row(types.InlineKeyboardButton(
            text='Спільний список',
            callback_data='authorslist'
        ))
    return help_buttons