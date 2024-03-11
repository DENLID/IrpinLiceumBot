from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from motor.core import AgnosticDatabase as MDB

from filters.filters import IsAdminChat, IsMsAdmin
import keyboards.keyboards as keyboards
import config


router = Router()


@router.message(CommandStart())
async def start(message: Message, db: MDB) -> None:
    print(message.chat.id)
    id = int(message.chat.id)

    if await db.users.count_documents({"_id": id}) == 0:
        await db.users.insert_one(
    {
        "_id": int(message.chat.id),
        "username": message.from_user.username,
        "airalert": "never",
        "tags": []
    })

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
async def news(message: Message, bot: Bot, command: CommandObject, db: MDB):
    text = command.args
    for u in await db.users.find({}):
        try:
            await bot.send_message(chat_id=u["_id"], text=text)
        except:
            pass

@router.message(Command('ban'), IsAdminChat())
async def ban(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    chat_id = int(args[0])

    user_exist = await db.users.find_one({"_id": chat_id})
    if user_exist != None:
        username = user_exist["username"]
        await db.ban_list.insert_one({
            "_id": id,
            "username": username
        })
        await message.answer(f"Користувачу з ID: <code>{chat_id}</code> успішно забанений ✅")
    else:
        await message.answer(f"Користувач з ID: <code>{chat_id}</code> не знайдений ❌")
        
@router.message(Command('unban'), IsAdminChat())
async def ban(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    chat_id = int(args[0])

    user_exist = await db.users.find_one({"_id": chat_id})
    if user_exist != None:
        username = user_exist["username"]
        await db.ban_list.delete_one({
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
async def add_tag(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    chat_id = int(args[0])
    tag = args[1]

    if await db.users.find_one({"_id": chat_id}) != None:
        await db.users.update_one({"_id": chat_id}, {"$push": {"tags": tag}})
        await message.answer(f"Користувачу з ID: <code>{chat_id}</code> успішно добавлений тег <code>{tag}</code> ✅")
    else:
        await message.answer(f"Користувач з ID: <code>{chat_id}</code> не знайдений ❌")

@router.message(Command('delete_tag'), IsAdminChat())
async def delete_tag(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    chat_id = int(args[0])
    tag = args[1]

    if await db.users.find_one({"_id": chat_id}) != None:
        await db.users.update_one({"_id": chat_id}, {"$pull": {"tags": tag}})
        await message.answer(f"Користувачу з ID: <code>{chat_id}</code> успішно забрно тег <code>{tag}</code> ✅")
    else:
        await message.answer(f"Користувач з ID: <code>{chat_id}</code> не знайдений ❌")

@router.message(Command('get_info'), IsAdminChat())
async def delete_tag(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    chat_id = int(args[0])

    data = await db.users.find_one({"_id": chat_id})

    if data != None:
        await message.answer(f"""
Інформація про користувача:
ID: <code>{data["_id"]}</code>
username: @{data["username"]}
airalert: {data["airalert"]}
tags: {data["tags"]}
""")
    else:
        await message.answer(f"Користувач з ID: <code>{chat_id}</code> не знайдений ❌")



@router.message(Command('getmyid'))
async def getmyid(message: Message):
    await message.answer(f"""
Ваш телеграм айді: <code>{message.from_user.id}</code>
Ваш телеграм чат айді: <code>{message.chat.id}</code>""")  



