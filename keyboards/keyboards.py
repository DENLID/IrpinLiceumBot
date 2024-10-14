from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import (
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    KeyboardButton
)

from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.filters.callback_data import CallbackData

def check_mark(str, data):
    if str == data:
        return "✅"
    else:
        return ""

badge_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Замовити', url="https://t.me/irpin_liceum_bot?start=backpack_badge")]])
buy_badge_kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="💬 Зв'язок з адмінами 💬", callback_data="comm")]])

back_menu = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Назад', callback_data="menu")]])
back_details = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Назад', callback_data="details")]])
back_help = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Назад', callback_data="help")]])
back_ms = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='🔙 Назад', callback_data="ms")]])

back_details_button = [InlineKeyboardButton(text='🔙 Назад', callback_data="details")]
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
        ),
        InlineKeyboardButton(
            text="📲 Додатково 📲",
            callback_data="details"
        )
    ]
])

details_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="📕 Електронні підручники 📕", 
            callback_data="books"
        )
    ],
    [
        InlineKeyboardButton(
            text="🔔 Розклад дзвінків 🔔",
            callback_data="dzvinki"
        )
    ],
    back_menu_button
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
    class_num = int(user["class"].split('-')[0])

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
    builder.button(text="🔙 Назад", callback_data="details")
    l = [3]*round(len(items)/3)
    l[len(l)-1] -= 1
    builder.adjust(*l)

    return builder.as_markup()


ms_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="1",
            callback_data="ms_1"
        ),
        InlineKeyboardButton(
            text="2", 
            callback_data="ms_2"
        )
    ],
    [
        InlineKeyboardButton(
            text="3", 
            callback_data="ms_3"
        ),
        InlineKeyboardButton(
            text="4", 
            callback_data="ms_4"
        )
    ],
    [
        InlineKeyboardButton(
            text="Надіслати ✅", 
            callback_data="ms_accept"
        )
    ]
])

confirm_person_kb = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(
            text="Email",
            callback_data="confirm_person_email"
        )
    ],
    [
        InlineKeyboardButton(
            text="Номер телефону", 
            callback_data="comming"
        )
    ]
])
