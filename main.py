from vkbottle.bot import Bot, Message
import os

bot = Bot(token=os.getenv("TOKEN"))

# Ловим ВСЁ из чатов сообществ
@bot.on.message()
async def all_messages(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    if text in ["!пинг", ".пинг", "пинг", "!ping"]:
        await message.answer("⚫ Onyx живой | 16.11.2025 | Работает в чатах сообществ!")

    if text in ["!помощь", "!help"]:
        await message.answer("⚫ Onyx полностью работает!")

print("Onyx запущен и ловит ВСЁ из чатов сообществ ⚫")
await bot.run_polling()
