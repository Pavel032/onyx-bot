# main.py
from vkbottle.bot import Bot, Message
import os

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# Замени на настоящий ID своего сообщества Onyx Чат-Менеджер
GROUP_ID = 233971978  # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

bot = Bot(
    token=os.getenv("TOKEN"),   # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
    group_ids=[GROUP_ID]        # ← вот так, с запятой после token!
)

@bot.on.chat_message(text="!пинг")
async def ping(message: Message):
    await message.answer("⚫ Onyx живой!\n2025 — полная победа!")

@bot.on.chat_message(text=["!помощь", "!help"])
async def help_cmd(message: Message):
    await message.answer("⚫ Onyx 100 % работает в чатах сообществ!")

print("Onyx запущен — всё идеально ⚫")
bot.run_polling()
