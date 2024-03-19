from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData
from update_info.update_info import alphabet_ukr

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
            text="📕 Електронні підручники 📕", 
            callback_data="books"
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

def book_subject_kb(user):
    all_class = [f"{n}-{l}" for n in range(11) for l in alphabet_ukr]
    class_num = int(next((c for c in all_class if c in user["tags"]), None).split('-')[0])

    items = [
        "Математика", "Анг. Мова",
        "Укр. Мова", "Укр. Літ.",
        "Технології", "Мистецтво",
        "Фізкультура"
    ]

    if class_num >= 2:
        items.remove("Мистецтво")
        items.extend(["Обр. Мис.", "Муз. Мис."])

    if class_num >= 3:
        items.append("Інформатика")

    if class_num >= 5:
        items.extend(["Історія", "Природознав.", "Осн. Здор."])

    if class_num >= 6:
        items.remove("Природознав.")
        items.extend(["Географія", "Біологія"])

    if class_num >= 7:
        items.remove("Математика")
        items.extend(["Алгебра", "Геометрія", "Хімія"])

    if class_num >= 8:
        items.remove("Обр. Мис.")
        items.remove("Муз. Мис.")
        items.append("Мистецтво")
    
    builder = InlineKeyboardBuilder()
    [builder.button(text=item, callback_data="comming") for item in items]
    builder.button(text="🔙 Назад", callback_data="menu")
    l = [3]*round(len(items)/3)
    l[len(l)-1] -= 1
    builder.adjust(*l)

    return builder.as_markup()