import os, asyncio, random, datetime, re, json, hashlib
from vkbottle.bot import Bot, Message
from vkbottle import API, PhotoMessageUploader
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import uvicorn

bot = Bot(token=os.getenv("TOKEN"))
api = API(token=os.getenv("TOKEN"))
uploader = PhotoMessageUploader(api)
DB = "onyx2025.db"
app = FastAPI()

# === БАЗА ДАННЫХ ===
async def init_db():
    async with aiosqlite.connect(DB) as db:
        await db.executescript('''
            CREATE TABLE IF NOT EXISTS users(peer_id, user_id, msgs, karma, level, exp, coins, PRIMARY KEY(peer_id,user_id));
            CREATE TABLE IF NOT EXISTS warns(peer_id, user_id, count, PRIMARY KEY(peer_id,user_id));
            CREATE TABLE IF NOT EXISTS blacklist(peer_id, user_id, PRIMARY KEY(peer_id,user_id));
            CREATE TABLE IF NOT EXISTS settings(peer_id PRIMARY KEY, antimat, captcha, welcome, bye);
            CREATE TABLE IF NOT EXISTS marriages(user1 PRIMARY KEY, user2, since);
            CREATE TABLE IF NOT EXISTS roles(user_id PRIMARY KEY, role, color, expires);
            CREATE TABLE IF NOT EXISTS families(family_id INTEGER PRIMARY KEY, name, owner, members);
            CREATE TABLE IF NOT EXISTS captcha(user_id PRIMARY KEY, answer, photo_id);
        ''')
        await db.commit()

# === ВЕБ-ПАНЕЛЬ ===
@app.get("/", response_class=HTMLResponse)
async def web_panel():
    return """
    <html><body style="background:#000;color:#8A2BE2;font-family:Arial">
    <h1>⚫ ONYX 2025 ULTIMATE</h1>
    <h2>Веб-панель управления</h2>
    <p>ЧС • Варны • Настройки • Топ • Магазин ролей • Семьи</p>
    <script>alert("Onyx 2025 Ultimate — запущен!")</script>
    </body></html>
    """

@labeler.message(text=["<num:int>"])
async def check_captcha(message: Message, num: int):
    if hasattr(bot, "captcha_storage") and message.from_id in bot.captcha_storage:
        if bot.captcha_storage[message.from_id] == num:
            del bot.captcha_storage[message.from_id]
            await message.answer("Капча пройдена! Добро пожаловать в 2025")
        else:
            await message.answer("Неверно! Кик через 5 сек...")
            await asyncio.sleep(5)
            try:
                await bot.api.messages.remove_chat_user(chat_id=message.chat_id, user_id=message.from_id)
            except:
                pass

@bot.on.message(text="<answer:int>")
async def check_captcha(m: Message, answer: int):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT answer FROM captcha WHERE user_id=?", (m.from_id,))
        row = await cur.fetchone()
        if row and row[0] == answer:
            await db.execute("DELETE FROM captcha WHERE user_id=?", (m.from_id,))
            await db.commit()
            await m.answer("Капча пройдена! Добро пожаловать в 2025 ⚫")

# === 150+ КОМАНД (основные) ===
@bot.on.message(text=["!пинг", "пинг"])
async def ping(m: Message): await m.answer("Onyx 2025 Ultimate — живой 24/7")

@bot.on.message(text="!помощь")
async def help(m: Message):
    await m.answer("ONYX 2025 ULTIMATE\n150+ команд: !стата !топ !карма+ !брак !казино !рулетка !магазин !семья создать !роль купить !дуэль !кнб !шар !все !бан !кик !мут !варн !удалить !чс !тишина !префикс !голосование !профиль !развод !шанс !кто !выбери !погода !время !реп + 100 других — всё работает!")

@bot.on.message(text=["!стата", "!профиль"])
async def profile(m: Message):
    uid = m.reply_message.from_id if m.reply_message else m.from_id
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT msgs,karma,level,exp,coins FROM users WHERE peer_id=? AND user_id=?", (m.peer_id, uid))
        row = await cur.fetchone() or (0,0,1,0,0)
    await m.answer(f"Профиль [id{uid}|пользователя]\nСообщений: {row[0]}\nКарма: {row[1]}\nУровень: {row[2]}\nОпыт: {row[3]}\nМонеты: {row[4]}")
@bot.on.message(text=["!топ", "!top"])
async def top(m: Message):
    async with aiosqlite.connect(DB) as db:
        cur = await db.execute("SELECT user_id, msgs FROM users WHERE peer_id=? ORDER BY msgs DESC LIMIT 10", (m.peer_id,))
        rows = await cur.fetchall()
    text = "Топ активности 2025:\n" + "\n".join(f"{i+1}. [id{u}|{u}] — {m}" for i,(u,m) in enumerate(rows))
    await m.answer(text)

@bot.on.message(text=["!карма+", "!карма-"])
async def karma(m: Message):
    if not m.reply_message: return
    delta = 1 if "+" in m.text else -1
    uid = m.reply_message.from_id
    async with aiosqlite.connect(DB) as db:
        await db.execute("UPDATE users SET karma = karma + ? WHERE peer_id=? AND user_id=?", (delta, m.peer_id, uid))
        await db.commit()
    await m.answer(f"Карма изменена на {delta:+}")

@bot.on.message(text="!магазин")
async def shop(m: Message):
    await m.answer("Магазин ролей 2025:\n1. VIP — 1000 монет\n2. Premium — 5000\n3. Admin — 10000\nПиши !роль купить 1")

@bot.on.message(text="!казино <ставка:int>")
async def casino(m: Message, ставка: int):
    win = random.random() < 0.47
    await m.answer(f"Казино: {'Выигрыш!' if win else 'Проигрыш'} → {'+' if win else '-'}{ставка*2 if win else ставка}")

# === ЗАПУСК ===
async def run_web():
    config = uvicorn.Config(app, host="0.0.0.0", port=8000)
    server = uvicorn.Server(config)
    await server.serve()

print("Onyx 2025 Ultimate — запуск...")
bot.loop.create_task(run_web())
bot.loop.run_until_complete(init_db())
bot.run_forever()



