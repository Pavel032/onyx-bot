from vkbottle.bot import Bot, Message
import os

bot = Bot(token=os.getenv("TOKEN"))

@bot.on.message()
async def handler(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    if text in ["!пинг", ".пинг", "пинг", "!ping"]:
        await message.answer("⚫ Onyx онлайн | 2025 | Полностью живой!")

    if text in ["!помощь", "!help", "помощь", "help"]:
        await message.answer("""⚫ Onyx • Чат-менеджер 2025

!пинг — проверка бота
!помощь — это меню

Скоро добавим всё остальное:
• !бан • !кик • !варн • антимат • статистика • топ • мини-приложение""")

print("Onyx полностью запущен ⚫")
bot.run_polling()   # ← без await !!!
