from aiogram.filters import Command, CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from pytz import timezone
from datetime import datetime
from pymongo import MongoClient
import json

from register import register
from states import Communication
from filters import IsAdmin, IsAdminChat, IsWadMessage, IsMsAdmin
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
    await message.answer_document(document=FSInputFile("/home/container/ms.xlsx"), caption="Список відсутніх учнів в школі")
    
@router.message(Command('news'))
async def news(message: Message, state: FSMContext):
    await state.set_state(Communication.news_state)
    await message.answer("Надішліть повідомлення яке отримають всі користувачі")

@router.message(Command('ban'), IsAdmin())
async def ban(message: Message, state: FSMContext):
    if message.chat.id == config.admin_group:
        id = int(message.text.split(maxsplit=1)[1])
        user_exist = users.find_one({"_id": id})
        if user_exist != None:
            username = user_exist["username"]
            ban_list.insert_one({
                "_id": id,
                "username": username
            })
            await message.answer("Користувач успішно забанений")
        else:
            await message.answer("Невірний ID користувача")
        
@router.message(Command('unban'), IsAdmin())
async def ban(message: Message):
    if message.chat.id == config.admin_group:
        id = int(message.text.split(maxsplit=1)[1])
        user_exist = users.find_one({"_id": id})
        if user_exist != None:
            username = user_exist["username"]
            ban_list.delete_one({
                "_id": id,
                "username": username
            })
            await message.answer("Користувач успішно розбанений")
        else:
            await message.answer("Невірний ID користувача")

@router.message(IsAdminChat())
async def handle_text(message: Message):
    try:
        text = message.reply_to_message.text
        start_index = text.find("ID: ") + len("ID: ")
        end_index = text.find(" | USERNAME:")
        id = text[start_index:end_index]
        await bot.copy_message(id, config.admin_group, message.message_id)
    except:
        print("Just message in admin chat...")

@router.message(Command('getmyid'))
async def getmyid(message: Message):
    await message.answer(f"Ваш телеграм айді: <code>{message.chat.id}</code> <code>{message.from_user.id}</code>")

@router.message(Communication.news_state)
async def news_state_func(message: Message):
    for username in config.msw_admins:
        if username == message.from_user.username:
            for u in users.find({}):
                try:
                    await bot.send_message(chat_id=u["_id"], text=message.text)
                except:
                    pass
    
    
@router.message(IsWadMessage(), IsMsAdmin())
async def wad_handler(message: Message):
    webdata = message.web_app_data.data
    data = json.loads(webdata)
    await message.answer(f"""
Клас: {data["class_number"]} - {data["class_letter"]}
Кількість учнів в класі: {data["students_number"]}
Кількість присутніх в класі: {int(data["students_number"])-int(data["ms_number"])}
Відсутні: {data["ms"]}
""", reply_markup=keyboards.ms_tf_func(data["class_letter"], int(data["class_number"]), data["students_number"], int(data["students_number"])-int(data["ms_number"]), data["ms"]))
    

@router.message(Communication.mess)
async def handle_text(message: Message):
    if ban_list.find_one({"_id": message.chat.id}) == None:
        text = f"""
{message.text}

ID: <code>{message.chat.id}</code> | USERNAME: @{message.from_user.username} |
"""
        if message.content_type == "text":
            await bot.send_message(chat_id=config.admin_group, text=text)
        if message.content_type == "photo":
            await bot.send_photo(chat_id=config.admin_group, photo=message.photo[-1].file_id, caption=text)
        if message.content_type == "video":
            await bot.send_video(chat_id=config.admin_group, video=message.video.file_id, caption=text)
        if message.content_type == "document":
            await bot.send_document(chat_id=config.admin_group, document=message.document.file_id, caption=text)
    else:
        await message.answer("""
Ви отривали бан, тому не можете 
надсилати повідомлення адміністраторам.
""")
