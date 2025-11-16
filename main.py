from vkbottle.bot import Bot, Message
import os

# Явно указываем group_id (это спасает от ошибки NoneType)
GROUP_ID = 233971978  # ← замени на ID своего сообщества Onyx Чат-Менеджер
# Как узнать ID: зайди в сообщество → в адресной строке будет club228571140 или public228571140 → цифры и есть ID

bot = Bot(token=os.getenv("TOKEN"), group_id=GROUP_ID)

@bot.on.chat_message(text="!пинг")
async def ping(message: Message):
    await message.answer("Onyx живой и полностью рабочий!\n2025 год — победа ⚫")

@bot.on.chat_message(text=["!помощь", "!help"])
async def help_cmd(message: Message):
    await message.answer("Onyx онлайн!\nВсе функции скоро будут добавлены")

print("Onyx запущен без ошибок — готов к работе ⚫")
bot.run_polling()
