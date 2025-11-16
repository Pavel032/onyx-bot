# main.py — работает в чатах сообществ без group_ids
from vkbottle.bot import Bot, Message
import os

bot = Bot(token=os.getenv("TOKEN"))  # Только token — ничего больше!

@bot.on.message()  # Ловим все сообщения, включая чаты сообществ
async def handler(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    if text in ["!пинг", "пинг", ".пинг", "!ping"]:
        await message.answer("⚫ Onyx живой!\n17.11.2025 — полная победа в чатах сообществ!")

    if text in ["!помощь", "!help"]:
        await message.answer("⚫ Onyx полностью онлайн!\nГотов к бою")

print("Onyx запущен — ждёт сообщений из чатов сообществ ⚫")

if name == "main":
    bot.run_forever()  # Стабильный запуск для 4.x
