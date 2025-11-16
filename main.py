import asyncio
import aiosqlite
import json
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import ChatPermissions

TOKEN = "vk1.a.shvMGIjJv63BUINdZTS2jXbVB8xUBEYgRCeOgz9dMTg-wQKvCHJUEFUuyEKJWGCel0UrUtmedlV5d46FtW0lkWfKjQGeagp5Z3CDtvyYd6z5inaKTXKHjyORgnznWP4Kn5RLqQlGTmxoqdo_bxARDJpVGRzha-pCvAX02jApDPDDhteoWqOLVp5frt6NHK1IPa4B2Hm2lF1WDkRue-m07Q"  # ← ВСТАВЬ СВОЙ ТОКЕН СЮДА ПОСЛЕ ДЕПЛОЯ (в переменной окружения)

bot = Bot(token=TOKEN, parse_mode="HTML")
dp = Dispatcher()

DB = "onyx.db"

async def get_db():
    db = await aiosqlite.connect(DB)
    await db.executescript("""
        CREATE TABLE IF NOT EXISTS settings (chat_id INTEGER PRIMARY KEY, data TEXT);
        CREATE TABLE IF NOT EXISTS blacklist (chat_id INT, user_id INT, reason TEXT);
        CREATE TABLE IF NOT EXISTS warns (chat_id INT, user_id INT, count INT);
        CREATE TABLE IF NOT EXISTS stats (chat_id INT, user_id INT, messages INT DEFAULT 0);
    """)
    await db.commit()
    return db

async def get_settings(chat_id):
    db = await get_db()
    cur = await db.execute("SELECT data FROM settings WHERE chat_id=?", (chat_id,))
    row = await cur.fetchone()
    await db.close()
    if row:
        return json.loads(row[0])
    default = {"prefix": "!", "antimat": True, "antilink": True, "anticaps": True, "warnkick": 3}
    await save_settings(chat_id, default)
    return default

async def save_settings(chat_id, data):
    db = await get_db()
    await db.execute("REPLACE INTO settings (chat_id, data) VALUES (?, ?)", (chat_id, json.dumps(data)))
    await db.commit()
    await db.close()

async def is_admin(message: types.Message):
    member = await bot.get_chat_member(message.chat.id, message.from_user.id)
    return member.status in ("administrator", "creator")

@dp.message(Command("помощь", "help"))
async def help_cmd(m: types.Message):
    await m.reply("""<b>Onyx • Чат-менеджер</b>

!бан @user [причина]
!кик @user
!варн @user
!удалить [кол-во]
!стата [@user]
!топ
!пинг
!префикс !""")

@dp.message(Command("пинг"))
async def ping(m: types.Message):
    await m.reply("⚫ <b>Onyx онлайн</b>")

@dp.message(Command("бан"))
async def ban(m: types.Message):
    if not await is_admin(m): return
    if not m.reply_to_message: return await m.reply("Ответь на сообщение")
    user = m.reply_to_message.from_user
    await bot.ban_chat_member(m.chat.id, user.id)
    await m.reply(f"⚫ Забанен {user.first_name}")

@dp.message(Command("кик"))
async def kick(m: types.Message):
    if not await is_admin(m): return
    if not m.reply_to_message: return
    user = m.reply_to_message.from_user
    await bot.ban_chat_member(m.chat.id, user.id)
    await bot.unban_chat_member(m.chat.id, user.id)
    await m.reply(f"⚫ Кикнут {user.first_name}")

@dp.message(Command("варн"))
async def warn(m: types.Message):
    if not await is_admin(m): return
    if not m.reply_to_message: return
    user = m.reply_to_message.from_user
    db = await get_db()
    await db.execute("INSERT INTO warns VALUES (?, ?, 1) ON CONFLICT(chat_id, user_id) DO UPDATE SET count = count + 1", (m.chat.id, user.id))
    await db.commit()
    async with db.execute("SELECT count FROM warns WHERE chat_id=? AND user_id=?", (m.chat.id, user.id)) as cur:
        count = (await cur.fetchone())[0]
    await m.reply(f"⚫ Предупреждение {count}/3")
    if count >= 3:
        await bot.ban_chat_member(m.chat.id, user.id)
        await m.reply(f"⚫ Автобан за 3 варна")
    await db.close()

@dp.message()
async def counter_and_antimat(m: types.Message):
    # Счётчик сообщений
    db = await get_db()
    await db.execute("INSERT INTO stats VALUES (?, ?, 1) ON CONFLICT(chat_id, user_id) DO UPDATE SET messages = messages + 1", (m.chat.id, m.from_user.id))
    await db.commit()
    await db.close()

    # Антимат (простой)
    if any(word in m.text.lower() for word in ["хуй", "пизд", "бля", "ебан"]):
        await m.delete()
        await m.answer("⚫ Мат запрещён")

async def main():
    await get_db()
    print("Onyx запущен ⚫")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())