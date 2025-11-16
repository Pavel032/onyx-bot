from vkbottle.bot import Bot, Message
import os

bot = Bot(token=os.getenv("TOKEN"))

@bot.on.message()
async def handler(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    if text in ["!пинг", ".пинг", "пинг", "!ping"]:
        await message.answer("⚫ Onyx онлайн | 2025 | 100 % живой!")

    if text in ["!помощь", "!help", "помощь"]:
        await message.answer("""⚫ Onyx • Чат-менеджер 2025

!пинг — проверка
Скоро добавим:
• !бан @user
• !кик @user  
• !варн @user (3 → автобан)
• антимат / антиссылки
• статистика / топ
• мини-приложение как у pxolly""")

print("Onyx полностью запущен ⚫")
await bot.run_polling()
