# main.py
from vkbottle.bot import Bot, Message
import os

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
GROUP_ID = 233971978  # твой ID сообщества
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

bot = Bot(
    token=os.getenv("TOKEN"),
    group_ids=[GROUP_ID]   # ← именно group_ids и обязательно в виде списка!
)

@bot.on.chat_message(text=["!пинг", "пинг", ".пинг"])
async def ping(message: Message):
    await message.answer("⚫ Onyx живой!\n17.11.2025 — полная победа!")

@bot.on.chat_message(text=["!помощь", "!help"])
async def help_cmd(message: Message):
    await message.answer("⚫ Onyx 100 % работает в чатах сообществ!")

print("Onyx запущен — всё идеально ⚫")
bot.run_polling()
