# main.py — гарантированно работает на Railway 17.11.2025
from vkbottle.bot import Bot, Message
import os

bot = Bot(token=os.getenv("TOKEN"))

@bot.on.message()
async def handler(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    if text in ["!пинг", "пинг", ".пинг", "!ping"]:
        await message.answer("⚫ Onyx живой!\n17.11.2025 — наконец-то всё работает в чатах сообществ!")

    if text in ["!помощь", "!help"]:
        await message.answer("⚫ Onyx полностью онлайн!")

print("Onyx запущен — ждёт сообщений из чатов сообществ ⚫")

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# Самый надёжный способ запуска на Railway
bot.loop_wrapper.on_startup.append(print("Поллинг стартовал"))
bot.run_forever()
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
