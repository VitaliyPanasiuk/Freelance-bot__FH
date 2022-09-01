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
        types.KeyboardButton(text="✅Прийняти")
    )
    home_buttons.add(
        types.KeyboardButton(text="❌Відхилити")
    )
    home_buttons.adjust(2)
    return home_buttons

def answer_request2():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.add(
        types.KeyboardButton(text="✅Прийняти замовлення")
    )
    home_buttons.add(
        types.KeyboardButton(text="❌Відхилити")
    )
    home_buttons.adjust(1)
    return home_buttons

def answer_speciality():
    home_buttons = ReplyKeyboardBuilder()
    home_buttons.row(
        types.KeyboardButton(text="Готово✅")
    )
    home_buttons.add(
        types.KeyboardButton(text="Біологія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Будівництво та цивільна інженерія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Видавництво та поліграфія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Географія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Геодезія та землеустрій")
    )
    home_buttons.add(
        types.KeyboardButton(text="Гідротехнічне будівництво, водна інженерія та водні технології")
    )
    home_buttons.add(
        types.KeyboardButton(text="Готельно-ресторанна справа")
    )
    home_buttons.add(
        types.KeyboardButton(text="Дизайн")
    )
    home_buttons.add(
        types.KeyboardButton(text="Дошкільна освіта")
    )
    home_buttons.add(
        types.KeyboardButton(text="Економіка")
    )
    home_buttons.add(
        types.KeyboardButton(text="Журналістика")
    )
    home_buttons.add(
        types.KeyboardButton(text="Інформаційна, бібліотечна та архівна справа")
    )
    home_buttons.add(
        types.KeyboardButton(text="Історія та археологія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Культурологія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Маркетинг")
    )
    home_buttons.add(
        types.KeyboardButton(text="Математика")
    )
    home_buttons.add(
        types.KeyboardButton(text="Медицина")
    )
    home_buttons.add(
        types.KeyboardButton(text="Міжнародне право")
    )
    home_buttons.add(
        types.KeyboardButton(text="Менеджмент")
    )
    home_buttons.add(
        types.KeyboardButton(text="Міжнародні відносини, суспільні комунікації та регіональні студії")
    )
    home_buttons.add(
        types.KeyboardButton(text="Міжнародні економічні відносини")
    )
    home_buttons.add(
        types.KeyboardButton(text="Музеєзнавство, пам’яткознавство")
    )
    home_buttons.add(
        types.KeyboardButton(text="Облік та оподаткування")
    )
    home_buttons.add(
        types.KeyboardButton(text="Підприємництво, торгівля та біржова діяльність")
    )
    home_buttons.add(
        types.KeyboardButton(text="Політологія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Початкова освіта")
    )
    home_buttons.add(
        types.KeyboardButton(text="Право")
    )
    home_buttons.add(
        types.KeyboardButton(text="Психологія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Публічне управління та адміністрування")
    )
    home_buttons.add(
        types.KeyboardButton(text="Релігієзнавство")
    )
    home_buttons.add(
        types.KeyboardButton(text="Середня освіта")
    )
    home_buttons.add(
        types.KeyboardButton(text="Соціологія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Статистика")
    )
    home_buttons.add(
        types.KeyboardButton(text="Стоматологія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Туризм")
    )
    home_buttons.add(
        types.KeyboardButton(text="Фізика та астрономія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Філологія (інші)")
    )
    home_buttons.add(
        types.KeyboardButton(text="Філологія (українська мова та література)")
    )
    home_buttons.add(
        types.KeyboardButton(text="Філософія")
    )
    home_buttons.add(
        types.KeyboardButton(text="Фінанси, банківська справа та страхування")
    )
    home_buttons.add(
        types.KeyboardButton(text="Харчові технології")
    )
    home_buttons.add(
        types.KeyboardButton(text="Хімія")
    )
    home_buttons.adjust(2)
    return home_buttons
