from vkbottle.bot import Bot, Message
import os

bot = Bot(token=os.getenv("TOKEN"))   # ← только token, без group_ids!

@bot.on.chat_message(text="!пинг")
async def ping(message: Message):
    await message.answer("⚫ Onyx живой!\n2025 — наконец-то полная победа!")

@bot.on.chat_message(text=["!помощь", "!help"])
async def help_cmd(message: Message):
    await message.answer("⚫ Onyx 100 % работает в чатах сообществ!")

print("Onyx запущен — финальная версия 2025 ⚫")
bot.run_polling()
