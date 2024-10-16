from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from motor.core import AgnosticDatabase as MDB
import aiocron

from filters.filters import IsAdmin, CheckArg, HasTag
import keyboards.keyboards as keyboards
from utils.utils import *
import config


router = Router()


@router.message(CommandStart(), CheckArg(None))
async def start(message: Message, db: MDB) -> None:
    id = int(message.chat.id)

    print({
        "id": id, 
        "name": message.from_user.full_name, 
        "username": message.from_user.username
    })


    if await db.users.count_documents({"_id": id}) == 0:
        await db.users.insert_one({
            "_id": id,
            "username": message.from_user.username,
            "airalert": "never",
            "balance": 0,
            "tags": [],
        })
    else:
        if (await db.users.find_one({"_id": id}))["username"] != message.from_user.username:
            await db.users.update_one({"_id": id}, {"$set": {"username": message.from_user.username}})

    await message.answer(text="""
Привіт, я телеграм бот
ірпінського ліцею №2!
Щоб перейти до меню
натисніть кнопку знизу 👇
""", reply_markup = keyboards.start_kb)


@router.message(Command('menu'))
async def menu(message: Message, ftype: str = None):
    text = """
<b>Меню</b>
"""
    if ftype == "call":
        await message.message.edit_text(text=text, reply_markup=keyboards.menu_kb)
    else:
        await message.answer(text=text, reply_markup=keyboards.menu_kb)

@router.message(Command('help'))
async def help(message: Message, ftype: str = None):
    text = "Виберіть запитання яке вас цікавить"
    if ftype == "call":
        await message.message.edit_text(text, reply_markup = keyboards.help_kb_menu)
    else:
        await message.answer(text, reply_markup = keyboards.help_kb_command)
    
    
@router.message(Command('ms'), HasTag("ms_admin"))
async def ms(message: Message, db: MDB, state: FSMContext, ftype: str = None):
    id = get_chat_id(message)

    user = await db.users.find_one({"_id": id})

    data = await state.get_data()

    text = f"""
<b>Редакція відсутніх учнів в класі {user['class']}.</b>

<b>1. Загальна кількість учнів в класі:</b> {data.get('students_number', '🚫')}
<b>2. Кількість відсутніх учнів в класі:</b> {data.get('ms_number', '🚫')}
<b>3. Кількість хворих із відсутніх:</b> {data.get('ms_number_hv', '🚫')}
<b>4. Відсутні:</b> {data.get('ms', '🚫')}

Виберіть пункт, який хочете редагувати:"""

    if ftype == "call":
        await message.message.edit_text(text, reply_markup=keyboards.ms_kb)
    else:
        await message.answer(text, reply_markup=keyboards.ms_kb)


@router.message(Command('ms_xlsx'), HasTag("ms_admin"))
async def ms_xlsx(message: Message):
    await message.answer_document(document=FSInputFile(config.path_ms), caption="Список відсутніх учнів в школі")
    
@router.message(Command('news'), IsAdmin())
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

@router.message(Command('ban'), IsAdmin())
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
        
@router.message(Command('unban'), IsAdmin())
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


@router.message(Command('add_tag'), IsAdmin())
async def add_tag(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    identifier = args[0]
    tag = args[1]

    user = get_user(identifier, db)

    if user != None:
        await db.users.update_one({"_id": user["_id"]}, {"$push": {"tags": tag}})
        await message.answer(f"Користувач успішно отримав тег <code>{tag}</code> ✅")
    else:
        await message.answer(f"Користувач не знайдений ❌")

@router.message(Command('remove_tag'), IsAdmin())
async def delete_tag(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    identifier = args[0]
    tag = args[1]

    user = get_user(identifier, db)

    if user != None:
        await db.users.update_one({"_id": user["_id"]}, {"$pull": {"tags": tag}})
        await message.answer(f"Користувач успішно отримав тег <code>{tag}</code> ✅")
    else:
        await message.answer(f"Користувач не знайдений ❌")

@router.message(Command('info'), IsAdmin())
async def delete_tag(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    identifier = args[0]

    user = get_user(identifier, db)

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

@router.message(Command('set'), IsAdmin())
async def confirm_person(message: Message, command: CommandObject, db: MDB):
    args = command.args.split()
    identifier = args[0]

    user = get_user(identifier, db)

    if user != None:
        await db.users.update_one({"_id": user["_id"]}, {"$set": {args[1]: args[2]}})
        await message.answer(f"Успішно ✅")
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
    try:
        await message.edit_text("Виберіть спосіб підтвердження особи", reply_markup=keyboards.confirm_person_kb)
    except:
        await message.answer("Виберіть спосіб підтвердження особи", reply_markup=keyboards.confirm_person_kb)

@router.message(Command('hbd'))
async def happy_birthday_denlid(message: Message, bot: Bot):
    bot.send_message(1055097116, """""")