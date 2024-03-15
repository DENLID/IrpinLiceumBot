from aiogram import F, Router
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from motor.core import AgnosticDatabase as MDB

from handlers.user_commands import send_menu, help_message
from utils.states import Communication
from update_info.update_info import update_info_ms
from keyboards.keyboards import MsCallback
import keyboards.keyboards as keyboards
import config


router = Router()

airalert_list = {
        "never": "<b>не</b> отримуєте повідомлення", 
        "st": "отримуєте повідомлення <b>в шкільний час</b>", 
        "always": "<b>завжди</b> отримуєте повідомлення"
}

@router.callback_query(MsCallback.filter(F.action == "ms_accept"))
async def ms_accept_callback(call: CallbackQuery, callback_data: MsCallback):
    update_info_ms(callback_data.class_letter, callback_data.class_number, 
                   callback_data.class_student, callback_data.present_students, 
                   callback_data.ms_number_hv, callback_data.ms_students)
    await call.message.edit_text("Список відсутніх учнів успішно оновлений ✅")

@router.callback_query(MsCallback.filter(F.data == "help_zvazok"))
@router.callback_query(MsCallback.filter(F.data == "comm_help"))
async def ms_accept_callback(call: CallbackQuery, callback_data: MsCallback):
    text="""
<b><i>Чому мені не відповіли адміни?</i></b> 

1. Бот знаходився на технійчній перерві. Зазвичай ми повідомляємо про технічну перерву.

2. Стався технічний збій. Попробуйте надіслати повідомлення ще раз.
                                     
<b>Якщо це вам не допомогло, то напишіть сюди: @denlid_uwu</b>
"""
    if call.data == "help_zvazok":
        await call.message.edit_text(text=text, reply_markup=keyboards.back_help)
    if call.data == "comm_help":
        await call.message.edit_text(text=text, reply_markup=keyboards.back_menu)

@router.callback_query()
async def query(call: CallbackQuery, state: FSMContext, db: MDB):
    if call.data == "menu":
        await send_menu(call, "call")
    if call.data == "comm":
        await state.set_state(Communication.mess)
        await call.message.edit_text(text="""
Надішліть ваше запитання або пропозицію. Якщо вам протягом 2 годин нічого не відповіли, то натиснітькнопку <b>Я не отримав відповіді</b>
""", reply_markup=keyboards.comm_kb)
            
    if call.data == "help":
        await help_message(call, "call")  

    if call.data == "help_command":
        await call.message.edit_text(text="""
<b><i>Всі команди бота</i></b>
        
/start - Запуск бота
/menu - Меню
/help - Допомога
""", reply_markup=keyboards.back_help)

    if "airalert" in call.data:
        airalert_type = call.data.replace("airalert_", "")
        if airalert_type in ["never", "st", "always"]:
            await db.users.update_one({"_id": call.message.chat.id}, {"$set": {"airalert": airalert_type}})
        user = await db.users.find_one({"_id": call.message.chat.id})
        print(user["airalert"])
        await call.message.edit_text(text=f"""
Виберіть коли ви хочете отримувати повідомлення повітряної тривоги/відбію. Наданий момент ви {airalert_list[user["airalert"]]}
""", reply_markup=keyboards.airalert_kb_func(user["airalert"]))
        
    if call.data == "ms_decline":
        await call.message.edit_text("Натисніть на кнопку Form, щоб перейти на форму заповнення відсутніх учнів в вашому класі.", 
reply_markup=keyboards.ms_kb)

    if call.data == "comming":
        await call.answer("В розробці", show_alert=True)

