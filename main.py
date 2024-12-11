from aiogram import types, Bot, Dispatcher
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import SessionLocal, User, init_db
from aiogram.filters import Command
from sqlalchemy.future import select
token = '6544378792:AAGB6I8iKDGdlvgQihHzJxziPnfTUHnPOgo'

bot = Bot(token=token)
dp = Dispatcher()


async def save_user(chat_id: int, first_name: str, last_name: str):
    async with SessionLocal() as session:
        async with session.begin():
            user = await session.get(User, chat_id)
            if not user:
                user = User(chat_id=chat_id, first_name=first_name, last_name=last_name)
                session.add(user)
            else:
                pass


@dp.message(Command('start'))
async def get_message(message: types.Message):
    try:
        await save_user(chat_id=message.chat.id, first_name=message.from_user.first_name, last_name=message.from_user.last_name)
        print("Save")
    except Exception as e:
        print(e)
    await message.answer(text="Salom")

@dp.message(Command('data'))
async def get_data(message: types.Message):
    async with SessionLocal() as session:
        result = await session.execute(select(User))
        users = result.scalars().all()
        if users:
            response = "\n".join(
                [f"ID: {user.id}, Ism: {user.first_name}, Familya: {user.last_name}, Chat ID: {user.chat_id}" for user in users]
            )
        else:
            response = "User lar mavjud emas"
        await message.answer(response)
async def main():
    await init_db()
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())