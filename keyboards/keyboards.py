from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from aiogram.filters.callback_data import CallbackData


def check_mark(str, data):
    if str == data:
        return "✅"
    else:
        return ""


back_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Назад', callback_data="menu")]])
back_help = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Назад', callback_data="help")]])

back_menu_button = [InlineKeyboardButton(text='🔙 Назад', callback_data="menu")]

start_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text = 'Перейти до меню',
            callback_data='menu'
        )
    ]
])

menu_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="💬 Зв'язок з адмінами 💬", 
            callback_data="comm"
        )
    ],
    [
        InlineKeyboardButton(
            text="🚨 Сповіщення повітряної тривоги 🚨", 
            callback_data="airalert"
        )
    ],
    [
        InlineKeyboardButton(
            text="🛠 Допомога 🛠", 
            callback_data="help"
        )
    ]
])

comm_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Я не отримав відповіді",
            callback_data="comm_help"
        )
    ],
    back_menu_button
])

help_kb_command = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Всі команди бота', callback_data="help_command")
    ],
    [
        InlineKeyboardButton(text='Чому на моє повідомлення нічого не відповіли?', callback_data="help_zvazok")
    ]
])

help_kb_menu = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Всі команди бота', callback_data="help_command")
    ],
    [
        InlineKeyboardButton(text='Мені не відповідають адміни', callback_data="help_zvazok")
    ],
    back_menu_button
])

ms_kb = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text="Form", web_app=WebAppInfo(url="https://denlid.github.io/IrpinLiceumBotWEBCITE/"))
    ]
])

def airalert_kb_func(data):
    airalert_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text=f"Ніколи {check_mark('never', data)}", callback_data="airalert_never")
        ],
        [
            InlineKeyboardButton(text=f"В шкільний час {check_mark('st', data)}", callback_data="airalert_st")
        ],
        [
            InlineKeyboardButton(text=f"Завжди {check_mark('always', data)}", callback_data="airalert_always")
        ],
        back_menu_button
    ])
    return airalert_kb


class MsCallback(CallbackData, prefix="ms"):
    action: str
    class_letter: str
    class_number: int
    class_student: int
    present_students: int
    ms_number_hv: int
    ms_students: str



def ms_confirm_kb(class_letter, class_number, class_student, present_students, ms_number_hv, ms_students):
    ms_tf_kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text='Так, все правильно ✅', callback_data=MsCallback(action="ms_accept",
                                                                                        class_letter=class_letter, class_number=class_number,
                                                                                        class_student=class_student, present_students=present_students,
                                                                                        ms_number_hv=ms_number_hv, ms_students=ms_students).pack())
        ],
        [
            InlineKeyboardButton(text='Ні, не правильно ❌', callback_data="ms_decline")
        ]
    ])
    return ms_tf_kb

to_comm_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="💬 Зв'язок з адмінами 💬", 
            callback_data="comm"
        )
    ],
])