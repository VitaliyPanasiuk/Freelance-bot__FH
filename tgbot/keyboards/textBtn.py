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
    home_buttons.add(
        types.KeyboardButton(text="Ece")
    )
    home_buttons.add(
        types.KeyboardButton(text="Тези")
    )
    home_buttons.add(
        types.KeyboardButton(text="Практичне завдання")
    )
    home_buttons.add(
        types.KeyboardButton(text="Презентація")
    )
    home_buttons.add(
        types.KeyboardButton(text="Інше")
    )
    home_buttons.adjust(2)
    return home_buttons

def answer_request():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="прийняти")
    )
    home_buttons.add(
        types.KeyboardButton(text="відхилити")
    )
    home_buttons.adjust(2)
    return home_buttons
def answer_request2():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="прийняти замовлення")
    )
    home_buttons.add(
        types.KeyboardButton(text="відхилити")
    )
    home_buttons.adjust(1)
    return home_buttons
