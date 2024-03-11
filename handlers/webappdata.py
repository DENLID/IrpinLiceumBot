from aiogram.filters import Command, CommandStart, CommandObject
from aiogram.types import Message, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram import Router, Bot, F
from motor.core import AgnosticDatabase as MDB

from filters.filters import IsAdminChat, IsMsAdmin, IsWadMessage
import keyboards.keyboards as keyboards
import config, json


router = Router()


@router.message(IsWadMessage())
async def wad_handler(message: Message, db: MDB):
    webdata = message.web_app_data.data
    data = json.loads(webdata)

    print((await db.users.find_one({"_id": int(message.chat.id)}))["tags"])
    print(f'{data["class_number"]}-{data["class_letter"]}')
    print(f'{data["class_number"]}-{data["class_letter"]}' in (await db.users.find_one({"_id": int(message.chat.id)}))["tags"])

    if f'{data["class_number"]}-{data["class_letter"]}' in (await db.users.find_one({"_id": int(message.chat.id)}))["tags"]:
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