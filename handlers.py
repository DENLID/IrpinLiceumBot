from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot
from pytz import timezone
from datetime import datetime
from pymongo import MongoClient
import json

from register import register
from update_info import update_info_ms
from states import Communication
import keyboards
import config

bot = Bot(config.bot_token, parse_mode="HTML")
router = Router()

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users
ban_list = cluster.ILdb.ban_list


@router.channel_post()
async def airalert_handler(message: Message):
    if message.chat.id == config.channel_all_to:
        ukraine_time = timezone('Europe/Kiev')
        dt = datetime.now(ukraine_time)
        weekday = dt.weekday()
        
        if weekday != 5 and weekday != 6 and datetime(dt.year, dt.month, dt.day, 8, 0, tzinfo=ukraine_time) <= dt <= datetime(dt.year, dt.month, dt.day, 18, 40, tzinfo=ukraine_time):
            for u in users.find({ "$or": [{"airalert": "st"}, {"airalert": "always"}]}):
                await message.copy_to(u["_id"]) # Надсилання користувачам
            await message.copy_to(config.channel_to) # Надсилання на канал
        else:
            for u in users.find({"airalert": "always"}):
                await message.copy_to(u["_id"])
    

@router.message(CommandStart())
async def start(message: Message):
    print(message.chat.id)
    await message.answer(text="""
Привіт, я телеграм бот
ірпінського ліцею №2!
Щоб перейти до меню
натисніть кнопку знизу 👇
""", reply_markup = keyboards.start_kb)
    register(message)


@router.message(Command('menu'))
async def menu(message: Message):
    await send_menu(message, "command")

async def send_menu(message, ftype):
    text = """
<b>Меню</b>
"""
    if ftype == "call":
        await message.message.edit_text(text=text, reply_markup=keyboards.menu_kb)
    elif ftype == "command":
        await message.answer(text=text, reply_markup=keyboards.menu_kb)

@router.message(Command('help'))
async def help(message: Message):
    await help_message(message, "command")

async def help_message(message, ftype):
    if ftype == "command":
        await message.answer("""
Виберіть запитання яке вас цікавить
""", reply_markup = keyboards.help_kb_command)
    elif ftype == "call":
        await message.message.edit_text("""
Виберіть запитання яке вас цікавить
""", reply_markup = keyboards.help_kb_menu)
    
    
@router.message(Command('ms'))
async def ms(message: Message):
    for username in config.msw_admins:
        if username == message.from_user.username:
            await message.answer("Натисніть на кнопку Form, щоб перейти на форму заповнення відсутніх учнів в вашому класі.", 
reply_markup=keyboards.ms_kb)

@router.message(Command('ms_xlsx'))
async def ms_xlsx(message: Message):
    await message.answer_document(document=FSInputFile("ms.xlsx"), caption="Список відсутніх учнів в школі")
    
@router.message(Command('news'))
async def news(message: Message, state: FSMContext):
    await state.set_state(Communication.news_state)
    await message.answer("Надішліть повідомлення яке отримають всі користувачі")

@router.message(Command('ban'))
async def ban(message: Message, state: FSMContext):
    id = int(message.text.split(maxsplit=1)[1])
    username = users.find_one({"_id": id})["username"]
    ban_list.insert_one({
        "_id": id,
        "username": username
    })
    await message.answer("Пользователь забанен")

@router.message(Communication.news_state)
async def news_state_func(message: Message):
    for username in config.msw_admins:
        if username == message.from_user.username:
            for u in users.find({}):
                try:
                    await bot.send_message(chat_id=u["_id"], text=message.text)
                except:
                    pass
    
async def send_to_admin(message):
    await message.forward(config.admin_group)
    sent = await message.forward(message.chat.id)
    await sent.delete()
    if sent.forward_from == None:
        await message.answer("""
У вас в налаштуваннях 
<b>Приватність і безпека 
(конфіденційність)</b> пересилання 
повідомлень вибрано <b>Ніхто</b>.
Тому адміни не зможуть вам відповісти.
""")

async def wad_message(message):
    webdata = message.web_app_data.data
    data = json.loads(webdata)
    await message.answer(f"""
Клас: {data["class_number"]} - {data["class_letter"]}
Кількість учнів в класі: {data["students_number"]}
Кількість присутніх в класі: {int(data["students_number"])-int(data["ms_number"])}
Відсутні: {data["ms"]}
""")
    update_info_ms("ms.xlsx", data["class_letter"], int(data["class_number"]), data["students_number"], int(data["students_number"])-int(data["ms_number"]), data["ms"])


@router.message(Communication.mess)
async def handle_text(message: Message):
    def ibl():
        for bl in ban_list.find({}):
            if message.chat.id == bl["_id"]:
                return True
    if message.web_app_data == None:
        if ibl() != True:
            await send_to_admin(message)
        else:
            await message.answer("""
Ви отривали бан, тому не можете 
надсилати повідомлення адміністраторам.
""")
    else:   
        await wad_message(message)

@router.message()
async def handle_text(message: Message):
    if message.web_app_data == None:
        if message.reply_to_message is not None and message.chat.id == config.admin_group:
            await message.copy_to(message.reply_to_message.forward_from.id)
    else:
        await wad_message(message)