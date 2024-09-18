from aiogram.filters import Command, CommandStart, CommandObject, or_f
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from motor.core import AgnosticDatabase as MDB

from filters.filters import IsAdminChat, IsMsAdmin, IsAdmin, CheckArg
import keyboards.keyboards as keyboards
from utils.utils import get_user_class
import config


router = Router()


@router.message(CommandStart(), CheckArg(None))
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
    await send_help(message, "command")

async def send_help(message, ftype: str):
    text = "Виберіть запитання яке вас цікавить"
    if ftype == "command":
        await message.answer(text, reply_markup = keyboards.help_kb_command)
    elif ftype == "call":
        await message.message.edit_text(text, reply_markup = keyboards.help_kb_menu)
    
    
@router.message(Command('ms'), IsMsAdmin())
async def ms(message: Message, db: MDB, state: FSMContext):
    await send_ms(message=message, db=db, state=state, ftype="command")

async def send_ms(message, db: MDB, state: FSMContext, ftype: str):
    try:
        id = message.chat.id
    except:
        id = message.message.chat.id

    user = await db.users.find_one({"_id": id})
    user_class = get_user_class(user)

    data = await state.get_data()

    def df(data_ce):
        try:
            return data[data_ce]
        except:
            return "🚫"

    text = f"""
<b>Редакція відсутніх учнів в класі {user_class}.</b>

<b>1. Загальна кількість учнів в класі:</b> {df("students_number")}
<b>2. Кількість відсутніх учнів в класі:</b> {df("ms_number")}
<b>3. Кількість хворих із відсутніх:</b> {df("ms_number_hv")}
<b>4. Відсутні:</b> {df("ms")}

Виберіть пункт, який хочете редагувати:"""

    if ftype == "command":
        await message.answer(text, reply_markup=keyboards.ms_kb)
    elif ftype == "call":
        await message.message.edit_text(text, reply_markup=keyboards.ms_kb)


@router.message(Command('ms_xlsx'))
async def ms_xlsx(message: Message):
    await message.answer_document(document=FSInputFile(config.path_ms), caption="Список відсутніх учнів в школі")
    
@router.message(Command('news'), or_f(IsAdminChat(), IsAdmin()))
async def news(message: Message, bot: Bot, command: CommandObject, db: MDB):
    text = command.args
    tag = text.split()[0]

    if tag == "all":
        users = db.users.find({})
        exist = 1
    else:
        users = db.users.find({"tags": {"$in": [tag]}})
        exist = await db.users.count_documents({"tags": {"$in": [tag]}})

    if exist != 0:
        async for user in users:
            try:
                await bot.send_message(chat_id=user["_id"], text=text.replace(tag, "", 1))
            except:
                pass
        await message.answer(f"Повідомлення успішно розіслано ✅")
    else:
        await message.answer(f"Користувачів з тегом <code>{tag}</code> не знайдено ❌")

@router.message(Command('ban'), or_f(IsAdminChat(), IsAdmin()))
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
        
@router.message(Command('unban'), or_f(IsAdminChat(), IsAdmin()))
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


@router.message(Command('add_tag'), or_f(IsAdminChat(), IsAdmin()))
async def add_tag(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    identifier = args[0]
    tag = args[1]

    if identifier.isdigit():
        chat_id = int(identifier)
        user = await db.users.find_one({"_id": chat_id})
    else:
        username = identifier.lstrip('@')
        user = await db.users.find_one({"username": username})

    if user != None:
        await db.users.update_one({"_id": user["_id"]}, {"$push": {"tags": tag}})
        await message.answer(f"Користувач успішно отримав тег <code>{tag}</code> ✅")
    else:
        await message.answer(f"Користувач не знайдений ❌")

@router.message(Command('remove_tag'), or_f(IsAdminChat(), IsAdmin()))
async def delete_tag(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    identifier = args[0]
    tag = args[1]

    if identifier.isdigit():
        user = await db.users.find_one({"_id": int(identifier)})
    else:
        username = identifier.lstrip('@')
        user = await db.users.find_one({"username": username})

    if user != None:
        await db.users.update_one({"_id": user["_id"]}, {"$pull": {"tags": tag}})
        await message.answer(f"Користувач успішно отримав тег <code>{tag}</code> ✅")
    else:
        await message.answer(f"Користувач не знайдений ❌")

@router.message(Command('info'), or_f(IsAdminChat(), IsAdmin()))
async def delete_tag(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    identifier = args[0]

    if identifier.isdigit():
        user = await db.users.find_one({"_id": int(identifier)})
    else:
        username = identifier.lstrip('@')
        user = await db.users.find_one({"username": username})

    if user != None:
        await message.answer(f"""
Інформація про користувача:
ID: <code>{user["_id"]}</code>
username: @{user["username"]}
airalert: {user["airalert"]}
tags: {user["tags"]}
""")
    else:
        await message.answer(f"Користувач не знайдений ❌")

@router.message(Command('getmyid'))
async def getmyid(message: Message):
    await message.answer(f"""
Ваш телеграм айді: <code>{message.from_user.id}</code>
Ваш телеграм чат айді: <code>{message.chat.id}</code>""")  

@router.message(Command('register_student'))
async def register_student(message: Message):
    await message.answer("В розробці 🛠")

@router.message(CommandStart(), CheckArg("backpack_badge"))
async def start_badge(message: Message, db: MDB, state: FSMContext):
    await message.answer("""
💛 Привіт, учні! 💙

🌟 Сьогодні ми запускаємо благодійну акцію! Відтепер у вас є можливість прикрасити свій рюкзак яскравими та стильними значками.

🌈 Половина прибутку піде на допомогу ЗСУ. Це не лише можливість зробити свій рюкзак унікальним, але і шанс зробити добру справу!

📲 Можливість придбати значки буде в нашому телеграм боті, натиснувши кнопку знизу та зв'язавшись з адмінами.

📅 Забрати свій значок можна буде у понеділок, з 10:00 до 14:00. Запрошуємо всіх бажаючих долучитися!

Разом до перемоги! 💛💙
""", reply_markup=keyboards.buy_badge_kb)

@router.message(Command('confirm_person'))
async def confirm_person(message: Message):
    await send_confirm_person(message)

async def send_confirm_person(message):
    try:
        await message.edit_text("Виберіть спосіб підтвердження особи", reply_markup=keyboards.confirm_person_kb)
    except:
        await message.answer("Виберіть спосіб підтвердження особи", reply_markup=keyboards.confirm_person_kb)