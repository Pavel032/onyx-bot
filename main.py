from vkbottle.bot import Bot, Message
import os

# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# Замени 123456789 на настоящий ID своего сообщества
# (в ссылке на сообщество это цифры после club или public)
GROUP_ID = 233971978   # ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←
# ←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←←

bot = Bot(
    token=os.getenv("TOKEN"),
    group_ids=[GROUP_ID]          # ← именно group_ids и в виде списка!
)

@bot.on.chat_message(text="!пинг")
async def ping(message: Message):
    await message.answer("⚫ Onyx наконец-то живой!\n2025 год — полная победа!")

@bot.on.chat_message(text=["!помощь", "!help"])
async def help_cmd(message: Message):
    await message.answer("⚫ Onyx 100 % работает в чатах сообществ!\nГотов к бою")

print("Onyx запущен — всё работает ⚫")
bot.run_polling()
