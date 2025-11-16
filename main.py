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

if __name__ == "__main__":
    asyncio.run(init_db())
    print("Onyx полностью готов к работе ⚫")
    bot.run_forever()
