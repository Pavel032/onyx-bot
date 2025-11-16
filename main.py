# main.py — гарантированно работает на Railway 17.11.2025
from vkbottle.bot import Bot, Message
import os

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# Только так в vkbottle 4.x — передаём токен как строку
bot = Bot(token=os.getenv("TOKEN"))

@bot.on.message()
async def handler(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    if text in ["!пинг", "пинг", ".пинг", "!ping"]:
        await message.answer("Onyx живой!\n17.11.2025 — всё работает в чатах сообществ!")

    if text in ["!помощь", "!help"]:
        await message.answer("Onyx полностью онлайн!")

print("Onyx запущен — ждём сообщений из чатов сообществ")

if __name__ == "__main__":
    bot.run_forever()   # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
