from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from pymongo import MongoClient

from register import register
from handlers import send_menu, help_message
from states import Communication
from update_info import update_info_ms
from mscallback import MsCallback
import keyboards
import config

router = Router()

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users


@router.callback_query()
async def query(call: CallbackQuery, state: FSMContext):
    if call.data == "menu":
        await send_menu(call, "call")
    if call.data == "comm":
        await state.set_state(Communication.mess)
        await call.message.edit_text(text="""
Надішліть ваше запитання або пропозицію.
Якщо вам протягом 2 годин нічого не відповіли,
то введіть команду /help та натисніть кнопку
<b>Чому на моє повідомлення нічого не відповіли?</b>""", reply_markup=keyboards.back_menu)
            
    if call.data == "help":
        await help_message(call, "call")  
    if call.data == "help_zvazok":
        await call.message.edit_text(text="""
<b><i>Чому на моє повідомлення нічого не відповіли?</i></b>
        
1. У вас в налаштуваннях 
<b>Приватнясть і безпека (кондефіційність)</b>
пересилання повідомлень стоїть <b>Ніхто</b>.

2. Бот знаходився на технійчній перерві.
Зазвичай ми повідомляємо про технічну перерву.

3. Стався технічний збій. Якщо це так,
то про це повідомлять адміни.""", reply_markup=keyboards.back_help)
    if call.data == "help_command":
        await call.message.edit_text(text="""
<b><i>Всі команди бота</i></b>
        
/start - Запуск бота
/menu - Меню
/help - Допомога
""", reply_markup=keyboards.back_help)

    l = {
        "never": "<b>не</b> отримуєте повідомлення", 
         "st": "отримуєте повідомлення <b>в шкільний час</b>", 
         "always": "<b>завжди</b> отримуєте повідомлення"
    }

    if call.data == "air_alert":
        user = users.find_one({"_id": call.message.chat.id})
        await call.message.edit_text(text=f"""
Виберіть коли ви хочете отримувати 
повідомлення повітряної тривоги
/відбію. Наданий момент ви 
{l[user["airalert"]]}""", reply_markup=keyboards.airalert_kb_func(user["airalert"]))
    for i in ["never", "st", "always"]:
        if call.data == f"airalert_{i}":
            users.update_one({"_id": call.message.chat.id}, {"$set": {"airalert": i}})
            user = users.find_one({"_id": call.message.chat.id})
            await call.message.edit_text(text=f"""
Виберіть коли ви хочете отримувати 
повідомлення повітряної тривоги
/відбію. Наданий момент ви 
{l[user["airalert"]]}""", reply_markup=keyboards.airalert_kb_func(user["airalert"]))

    if call.data == "ms_decline":
        await call.message.answer("Натисніть на кнопку Form, щоб перейти на форму заповнення відсутніх учнів в вашому класі.", 
reply_markup=keyboards.ms_kb)

    if call.data == "comming":
        await call.answer("В розробці", show_alert=True)


@router.callback_query(MsCallback.filter(F.action == "ms_accept"))
async def ms_accept_callback(call: CallbackQuery, callback_data: MsCallback):
    update_info_ms(callback_data.class_letter, callback_data.class_number, 
                   callback_data.class_student, callback_data.present_students, 
                   callback_data.ms_number_hv, callback_data.ms_students)
