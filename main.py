import logging
import asyncio
import os
import aiosqlite
from vkbottle.bot import Bot, Message
from vkbottle.modules import logger

# Настройка логирования (чтобы не было предупреждений в логах Railway)
logging.basicConfig(level=logging.INFO)

# Твой токен из переменной Railway
bot = Bot(token=os.getenv("TOKEN"))

# База данных для варнов, статистики и ЧС
DB = "onyx.db"

async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS warns (peer_id INTEGER, user_id INTEGER, count INTEGER DEFAULT 1, PRIMARY KEY(peer_id, user_id));
            CREATE TABLE IF NOT EXISTS blacklist (peer_id INTEGER, user_id INTEGER, reason TEXT, until TIMESTAMP);
            CREATE TABLE IF NOT EXISTS stats (peer_id INTEGER, user_id INTEGER, messages INTEGER DEFAULT 1, PRIMARY KEY(peer_id, user_id));
        """)
        await db.commit()

# Проверка, админ ли пользователь
async def is_admin(message: Message):
    try:
        members = await bot.api.messages.get_conversation_members(peer_id=message.peer_id, fields="is_admin")
        return any(m.member_id == message.from_id and m.is_admin for m in members.items)
    except:
        return False

# Команды
@bot.on.message(text=["!пинг", "!ping", "пинг"])
async def ping(message: Message):
    await message.answer("⚫ Onyx онлайн | 2025 | Полный клон pxolly готов!")

@bot.on.message(text=["!помощь", "!help"])
async def help_cmd(message: Message):
    help_text = """
⚫ Onyx • Чат-менеджер 2025

Модерация (только админы):
!бан @user [причина] [1ч/1д/7д] — бан
!разбан @user — разбан
!кик @user — кик
!варн @user [причина] — варн (3 → бан)
!разварн @user — снять варн
!удалить [число] — удалить последние сообщения
!чс — список ЧС

Настройки:
!антимат вкл/выкл — антимат
!префикс . — сменить префикс

Инфо:
!стата [@user] — статистика
!топ — топ активных
!пинг — тест

Аддоны и мини-приложение — в настройках группы.
    """
    await message.answer(help_text)

@bot.on.message(text="!бан")
async def ban(message: Message):
    if not await is_admin(message):
        return await message.answer("Только админы могут банить.")
    if not message.reply_to_message:
        return await message.answer("Ответь на сообщение пользователя.")
    user = message.reply_to_message.from_id
    reason = message.text.split(" ", 2)[2] if len(message.text.split()) > 2 else "Без причины"
    time = message.text.split(" ")[2] if len(message.text.split()) > 2 and message.text.split()[2] in ["1ч", "1д", "7д"] else "навсегда"
    
    # Добавляем в ЧС
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT OR REPLACE INTO blacklist VALUES (?, ?, ?, ?)", (message.peer_id, user, reason, time))
        await db.commit()
    
    await bot.api.messages.remove_chat_user(message.peer_id, user)
    await message.answer(f"⚫ {user} забанен по причине: {reason} ({time})")

@bot.on.message(text="!кик")
async def kick(message: Message):
    if not await is_admin(message):
        return
    if not message.reply_to_message:
        return await message.answer("Ответь на сообщение.")
    user = message.reply_to_message.from_id
    await bot.api.messages.remove_chat_user(message.peer_id, user)
    await bot.api.messages.add_chat_user(message.peer_id, user)
    await message.answer(f"⚫ {user} кикнут.")

@bot.on.message(text="!варн")
async def warn(message: Message):
    if not await is_admin(message):
        return
    if not message.reply_to_message:
        return await message.answer("Ответь на сообщение.")
    user = message.reply_to_message.from_id
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT OR REPLACE INTO warns VALUES (?, ?, (SELECT count FROM warns WHERE peer_id=? AND user_id=?)+1)", (message.peer_id, user, message.peer_id, user))
        await db.commit()
        cur = await db.execute("SELECT count FROM warns WHERE peer_id=? AND user_id=?", (message.peer_id, user))
        count = (await cur.fetchone())[0]
    
    await message.answer(f"⚫ Варн {count}/3 для {user}")
    if count >= 3:
        await ban(message)  # Автобан
@bot.on.message(text="!стата")
async def stat(message: Message):
    target = message.reply_to_message.from_id if message.reply_to_message else message.from_id
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT messages FROM stats WHERE peer_id=? AND user_id=?", (message.peer_id, target))
        row = await cur.fetchone()
        msgs = row[0] if row else 0
    await message.answer(f"⚫ Сообщений: {msgs}")

@bot.on.message(text="!топ")
async def top(message: Message):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT user_id, messages FROM stats WHERE peer_id=? ORDER BY messages DESC LIMIT 10", (message.peer_id,))
        rows = await cur.fetchall()
    text = "⚫ Топ активных:\n"
    for row in rows:
        text += f"• {row[1]} сообщений ({row[0]})\n"
    await message.answer(text or "⚫ Топ пустой")

# Авто-модерация (антимат)
@bot.on.message()
async def automod(message: Message):
    if message.from_id == bot.api.group_id:
        return  # Не модерируем сообщения бота
    bad_words = ["хуй", "пизд", "бля", "ебан", "пидор", "сука"]  # Добавь свои
    if any(word in message.text.lower() for word in bad_words):
        await message.delete()
        await message.answer("⚫ Мат запрещён!")

# Счётчик сообщений
@bot.on.message()
async def count_stats(message: Message):
    if message.from_id == bot.api.group_id:
        return
    async with aiosqlite.connect(DB) as db:
        await db.execute("INSERT OR REPLACE INTO stats VALUES (?, ?, (SELECT messages FROM stats WHERE peer_id=? AND user_id=?)+1)", (message.peer_id, message.from_id, message.peer_id, message.from_id))
        await db.commit()

# ——— ДОБАВЬ ЭТО В КОНЕЦ main.py ———

# Удаление последних N сообщений
@bot.on.message(text="!удалить <amount:int>")
async def delete_messages(message: Message, amount: int):
    if not await is_admin(message):
        return
    if amount < 1 or amount > 100:
        return await message.answer("⚫ Укажи от 1 до 100")
    msgs = await bot.api.messages.get_history(peer_id=message.peer_id, count=amount + 1)
    ids = [m.id for m in msgs.items if m.id != message.id][:amount]
    if ids:
        await bot.api.messages.delete(message_ids=ids, delete_for_all=True)
    await message.answer(f"⚫ Удалено {len(ids)} сообщений")

# Список ЧС
@bot.on.message(text="!чс")
async def blacklist_list(message: Message):
    if not await is_admin(message):
        return
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT user_id, reason FROM blacklist WHERE peer_id=?", (message.peer_id,))
        rows = await cur.fetchall()
    if not rows:
        return await message.answer("⚫ ЧС пуст")
    text = "⚫ Чёрный список:\n"
    for uid, reason in rows:
        text += f"• [id{uid}|{uid}] — {reason}\n"
    await message.answer(text)

# Разбан
@bot.on.message(text="!разбан <user_id:int>")
async def unban(message: Message, user_id: int):
    if not await is_admin(message):
        return
    async with aiosqlite.connect(DB) as db:
        await db.execute("DELETE FROM blacklist WHERE peer_id=? AND user_id=?", (message.peer_id, user_id))
        await db.commit()
    await message.answer(f"⚫ {user_id} разбанен")

# Снять варн
@bot.on.message(text="!разварн <user_id:int>")
async def unwarn(message: Message, user_id: int):
    if not await is_admin(message):
        return
    async with aiosqlite.connect(DB) as db:
        await db.execute("DELETE FROM warns WHERE peer_id=? AND user_id=?", (message.peer_id, user_id))
        await db.commit()
    await message.answer(f"⚫ Снят варн у {user_id}")

# Антимат вкл/выкл
@bot.on.message(text=["!антимат вкл", "!антимат выкл"])
async def antimat_toggle(message: Message):
    if not await is_admin(message):
        return
    state = "вкл" in message.text.lower()
    # Можно хранить в БД, но для простоты используем файл
    with open("antimat.txt", "w") as f:
        f.write("1" if state else "0")
    await message.answer(f"⚫ Антимат {'включён' if state else 'выключён'}")

# Проверка антимат-файла
def antimat_enabled():
    try:
        return open("antimat.txt").read().strip() == "1"
    except:
        return False

# Расширенный антимат
@bot.on.message()
async def antimat(message: Message):
    if antimat_enabled() and any(word in message.text.lower() for word in ["хуй", "пизд", "ебан", "бля", "пидор", "сука", "шлюха", "гнида"]):
        await message.delete()
        await message.answer(f"⚫ @id{message.from_id}(Мат запрещён!)")

# Префикс (простая смена)
@bot.on.message(text="!префикс <prefix>")
async def change_prefix(message: Message, prefix: str):
    if not await is_admin(message):
        return
    with open("prefix.txt", "w", encoding="utf-8") as f:
        f.write(prefix)
    await message.answer(f"⚫ Префикс изменён на {prefix}")

# Чтение префикса
def get_prefix():
    try:
        return open("prefix.txt", encoding="utf-8").read().strip() or "!"
    except:
        return "!"

# Пример использования префикса (можно расширить все команды)
@bot.on.message(text=f"{get_prefix()}пинг")
async def ping_with_prefix(message: Message):
    await message.answer("⚫ Onyx живой с новым префиксом!")

# ——— КОНЕЦ ДОБАВЛЕНИЯ ———

print("Onyx полностью готов к работе")

# Инициализация БД и запуск бота — без if name и без asyncio.run!
bot.loop.run_until_complete(init_db())
bot.run_forever()




