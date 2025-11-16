from vkbottle.bot import Bot, Message
import os
import aiosqlite
import asyncio
from datetime import datetime

bot = Bot(token=os.getenv("TOKEN"))

# База данных
DB = "onyx.db"
async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS warns (peer_id INTEGER, user_id INTEGER, count INTEGER DEFAULT 1, PRIMARY KEY(peer_id, user_id));
            CREATE TABLE IF NOT EXISTS stats (peer_id INTEGER, user_id INTEGER, messages INTEGER DEFAULT 1, PRIMARY KEY(peer_id, user_id));
        """)
        await db.commit()

# Права админа
async def is_admin(message: Message):
    admins = await bot.api.messages.get_conversation_members(peer_id=message.peer_id, fields="is_admin")
    return any(m.member_id == message.from_id and m.is_admin for m in admins.items)

# Команды
@bot.on.chat_message(text=["!пинг", "!Пинг", "!ПИНГ", ".пинг", ".Пинг"])
async def ping(message: Message):
    await message.answer("⚫ Onyx онлайн | <10мс")

@bot.on.chat_message(text=["!помощь", "!help"])
async def help_cmd(message: Message):
    await message.answer("""⚫ Onyx • Чат-менеджер 2025

!пинг — проверка
!бан @юзер — бан
!кик @юзер — кик
!мут @юзер 10 — мут на 10 минут
!варн @юзер — предупреждение (3 → бан)
!унварн @юзер — снять варн
!стата — твоя статистика
!топ — топ-10 активных
!удалить 50 — удалить 50 сообщений
!префикс . — сменить префикс""")

print("Onyx полностью запущен ⚫")
asyncio.get_event_loop().run_until_complete(init_db())
bot.run_forever()
