from vkbottle.bot import Bot, Message
import os

# Явно указываем group_id — это обходит всю ошибку
GROUP_ID = 233971978  # ← твой ID сообщества Onyx Чат-Менеджер

bot = Bot(token=os.getenv("TOKEN"), group_id=GROUP_ID)

@bot.on.chat_message(text=["!пинг", "пинг"])
async def ping(message: Message):
    await message.answer("Onyx живой!\n17.11.2025 — полная победа в чатах сообществ!")

@bot.on.chat_message(text=["!помощь", "!help"])
async def help_cmd(message: Message):
    await message.answer("Onyx 100 % работает!")

print("Onyx запущен — готов к работе в чатах сообществ")
bot.run_polling()
