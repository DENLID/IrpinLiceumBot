from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from pytz import timezone
from datetime import datetime
from pymongo import MongoClient
import json

from utils.states import Communication
from filters.filters import IsAdminChat, IsWadMessage, IsMsAdmin
import keyboerds.keyboards as keyboards
import config


router = Router()

cluster = MongoClient(config.mongo_api)
users = cluster.ILdb.users
ban_list = cluster.ILdb.ban_list


@router.message(CommandStart())
async def start(message: Message) -> None:
    print(message.chat.id)
    await message.answer(text="""
Привіт, я телеграм бот
ірпінського ліцею №2!
Щоб перейти до меню
натисніть кнопку знизу 👇
""", reply_markup = keyboards.start_kb)


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
    
    
@router.message(Command('ms'), IsMsAdmin())
async def ms(message: Message):
    await message.answer("Натисніть на кнопку Form, щоб перейти на форму заповнення відсутніх учнів в вашому класі.", 
reply_markup=keyboards.ms_kb)

@router.message(Command('ms_xlsx'))
async def ms_xlsx(message: Message):
    await message.answer_document(document=FSInputFile(config.path_ms), caption="Список відсутніх учнів в школі")
    
@router.message(Command('news',), IsAdminChat())
async def news(message: Message, state: FSMContext, bot: Bot, command: CommandObject):
    text = command.args
    for u in users.find({}):
        try:
            await bot.send_message(chat_id=u["_id"], text=text)
        except:
            pass

@router.message(Command('ban'), IsAdminChat())
async def ban(message: Message, command: CommandObject):
    args = command.args.split()
    chat_id = int(args[0])

    user_exist = users.find_one({"_id": chat_id})
    if user_exist != None:
        username = user_exist["username"]
        ban_list.insert_one({
            "_id": id,
            "username": username
        })
        await message.answer(f"Користувачу з ID: <code>{chat_id}</code> успішно забанений ✅")
    else:
        await message.answer(f"Користувач з ID: <code>{chat_id}</code> не знайдений ❌")
        
@router.message(Command('unban'), IsAdminChat())
async def ban(message: Message, command: CommandObject):
    args = command.args.split()
    chat_id = int(args[0])

    user_exist = users.find_one({"_id": chat_id})
    if user_exist != None:
        username = user_exist["username"]
        ban_list.delete_one({
            "_id": chat_id,
            "username": username
        })
        await message.answer(f"Користувачу з ID: <code>{chat_id}</code> успішно розбанений ✅")
    else:
        await message.answer(f"Користувач з ID: <code>{chat_id}</code> не знайдений ❌")

@router.message(Command('uchcom'), IsAdminChat())
async def uchcom(message: Message, bot: Bot):
    
    await bot.send_message(chat_id=None)

@router.message(Command('add_tag'), IsAdminChat())
async def add_tag(message: Message, command: CommandObject):
    args = command.args.split()
    chat_id = int(args[0])
    tag = args[1]

    if users.find_one({"_id": chat_id}) != None:
        users.update_one({"_id": chat_id}, {"$push": {"tags": tag}})
        await message.answer(f"Користувачу з ID: <code>{chat_id}</code> успішно добавлений тег <code>{tag}</code> ✅")
    else:
        await message.answer(f"Користувач з ID: <code>{chat_id}</code> не знайдений ❌")

@router.message(Command('delete_tag'), IsAdminChat())
async def delete_tag(message: Message, command: CommandObject):
    args = command.args.split()
    chat_id = int(args[0])
    tag = args[1]

    if users.find_one({"_id": chat_id}) != None:
        users.update_one({"_id": chat_id}, {"$pull": {"tags": tag}})
        await message.answer(f"Користувачу з ID: <code>{chat_id}</code> успішно забрно тег <code>{tag}</code> ✅")
    else:
        await message.answer(f"Користувач з ID: <code>{chat_id}</code> не знайдений ❌")

@router.message(Command('get_info'), IsAdminChat())
async def delete_tag(message: Message, command: CommandObject):
    args = command.args.split()
    chat_id = int(args[0])

    data = users.find_one({"_id": chat_id})

    if data != None:
        await message.answer(f"""
Інформація про користувача:
ID: {data["_id"]}
username: {data["username"]}
airalert: {data["airalert"]}
tags: {data["tags"]}
""")
    else:
        await message.answer(f"Користувач з ID: <code>{chat_id}</code> не знайдений ❌")

@router.message(IsAdminChat())
async def handle_text(message: Message, bot: Bot):
    try:
        text = message.reply_to_message.text
        start_index = text.find("ID: ") + len("ID: ")
        end_index = text.find(" | USERNAME:")
        id = text[start_index:end_index]
        await bot.copy_message(id, config.admin_group, message.message_id)
    except:
        print("Just reply message in admin chat...")

@router.message(Command('getmyid'))
async def getmyid(message: Message):
    await message.answer(f"""
Ваш телеграм айді: <code>{message.from_user.id}</code>
Ваш телеграм чат айді: <code>{message.chat.id}</code>""")  


@router.message(IsWadMessage(), IsMsAdmin())
async def wad_handler(message: Message):
    webdata = message.web_app_data.data
    data = json.loads(webdata)
    if [f'{data["class_number"]}-{data["class_letter"]}'] in users.find_one({"_id": int(message.chat.id)})["tags"]:
        await message.answer(f"""
Клас: {data["class_number"]} - {data["class_letter"]}
Кількість учнів в класі: {data["students_number"]}
Кількість присутніх в класі: {int(data["students_number"])-int(data["ms_number"])}
Кількість відсутніх в класі: {data["ms_number"]}
Кількість хворих із відсутніх: {data["ms_number_hv"]}
Відсутні: {data["ms"]}
""", reply_markup=keyboards.ms_tf_func(data["class_letter"], int(data["class_number"]), data["students_number"], int(data["students_number"])-int(data["ms_number"]), data["ms_number_hv"], data["ms"]))
    else:
        await message.answer(f'Вибачте але ви не можете редагувати відсутніх в класі {data["class_number"]} - {data["class_letter"]}', reply_markup=keyboards.comm_kb)

@router.message(Communication.mess)
async def handle_text(message: Message, bot: Bot):
    if ban_list.find_one({"_id": message.chat.id}) == None:
        text = f"""
{message.text}
{message.caption}

ID: <code>{message.chat.id}</code> | USERNAME: @{message.from_user.username} |
""".replace("""None\nNone\n""", "").replace("None\n", "")
#.replace("""
#None
#None

#""", "").replace("None", "")
        
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
