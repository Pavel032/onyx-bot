from vkbottle.bot import Bot, Message
import os
import asyncio

bot = Bot(token=os.getenv("TOKEN"))

@bot.on.message()  # ловит ВСЁ, включая чаты сообществ
async def handler(message: Message):
    if not message.text:
        return
    
    text = message.text.strip().lower()

    if text in ["!пинг", ".пинг", "пинг", "!ping"]:
        await message.answer("Onyx живой | 17.11.2025 | Работает в чатах сообществ!")

    if text in ["!помощь", "!help", "help"]:
        await message.answer("Onyx полностью работает!\nСкоро добавим все команды")

print("Onyx запущен и ловит сообщения из чатов сообществ")

# Правильный запуск
asyncio.run(bot.run_polling())
