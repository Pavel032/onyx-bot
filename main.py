from vkbottle.bot import Bot, Message
import os

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# В 4-й версии Bot принимает именно api, а не token напрямую
from vkbottle import API
api = API(token=os.getenv("TOKEN"))
bot = Bot(api=api)
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

@bot.on.message()
async def handler(message: Message):
    if not message.text:
        return

    text = message.text.strip().lower()

    if text in ["!пинг", "пинг", ".пинг", "!ping"]:
        await message.answer("⚫ Onyx наконец-то живой!\n17.11.2025 — полная победа в чатах сообществ!")

    if text in ["!помощь", "!help"]:
        await message.answer("⚫ Onyx 100% работает!")

print("Onyx запущен — ждём сообщений из чатов сообществ ⚫")

if name == "main":
    bot.run_forever()
