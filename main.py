import os
from vkbottle import API, Bot

token = os.getenv("TOKEN")
api = API(token)
bot = Bot(api=api)

@bot.on.chat_message(text=["!пинг", "!Пинг", "!ПИНГ", ".пинг", "пинг", "!ping"])
async def ping(message):
    await message.answer("⚫ Onyx наконец-то живой!\n2025 год, полная победа!")

@bot.on.chat_message(text=["!помощь", "!help"])
async def help_cmd(message):
    await message.answer("⚫ Onyx работает на 100%!\nГотов к бою!")

print("Onyx запущен — финальная версия ⚫")
bot.run_forever()
