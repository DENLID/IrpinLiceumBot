from aiogram.types import Message
from aiogram import Router, Bot, F
from motor.core import AgnosticDatabase as MDB

from utils.states import Communication
from filters.filters import IsAdminChat
import config


router = Router()


@router.message(IsAdminChat())
async def handle_text(message: Message, bot: Bot):
    try:
        text = message.reply_to_message.text
        if text == None:
            text = message.reply_to_message.caption
        start_index = text.find("ID: ") + len("ID: ")
        end_index = text.find(" | USERNAME:")
        id = text[start_index:end_index]
        await bot.copy_message(id, config.admin_group, message.message_id)
    except:
        print("Just reply message in admin chat...")
        

@router.message(Communication.mess)
async def handle_text(message: Message, bot: Bot, db: MDB):
    if await db.ban_list.find_one({"_id": message.chat.id}) == None:
        text = f"""
{message.text}
{message.caption}

ID: <code>{message.chat.id}</code> | USERNAME: @{message.from_user.username} |
""".replace("""None\nNone\n""", "").replace("None\n", "")      
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
Ви отривали бан, тому не можете надсилати повідомлення адміністраторам.
""")